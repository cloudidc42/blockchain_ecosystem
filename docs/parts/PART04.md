# PART04 - Database Design & Schema

> **เนื้อหา**: PostgreSQL Schema, ClickHouse Analytics, Indexing Strategy, Migrations with Alembic
>
> **เป้าหมาย**: ออกแบบและ implement database schema ที่ scalable สำหรับ Blockchain Explorer
>
> **ระยะเวลา**: 6-10 ชั่วโมง
>
> **Prerequisites**: PART01, PART02, PostgreSQL และ ClickHouse basics

---

## 📑 สารบัญ

1. [Database Architecture](#database-architecture)
2. [PostgreSQL Schema Design](#postgresql-schema-design)
3. [ClickHouse Analytics Schema](#clickhouse-analytics-schema)
4. [Indexing Strategy](#indexing-strategy)
5. [Migrations with Alembic](#migrations-with-alembic)
6. [Query Optimization](#query-optimization)
7. [แบบฝึกหัด](#แบบฝึกหัด)

---

## Database Architecture

### 1.1 Overview

Blockchain Explorer ใช้ **Dual Database Architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│                    Blockchain Explorer                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐      ┌──────────────┐     ┌──────────┐  │
│  │   Indexer    │─────►│ PostgreSQL   │◄────│   API    │  │
│  │   (ETL)      │      │   (OLTP)     │     │ (FastAPI)│  │
│  └──────────────┘      └──────────────┘     └──────────┘  │
│         │                      │                           │
│         │                      │                           │
│         ▼                      ▼                           │
│  ┌──────────────┐      ┌──────────────┐                   │
│  │ ClickHouse   │◄─────│  Analytics   │                   │
│  │ (Analytics)  │      │   Pipeline   │                   │
│  └──────────────┘      └──────────────┘                   │
│         │                                                  │
│         ▼                                                  │
│  ┌──────────────┐                                         │
│  │   Grafana    │                                         │
│  │ (Dashboard)  │                                         │
│  └──────────────┘                                         │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Why Dual Database?

**PostgreSQL (OLTP - Online Transaction Processing)**:
- ✅ ACID compliance (data integrity)
- ✅ Complex queries with JOINs
- ✅ Real-time reads/writes
- ✅ Strong consistency
- ❌ Not optimal for analytics on large datasets

**ClickHouse (OLAP - Online Analytical Processing)**:
- ✅ Column-oriented storage (fast aggregations)
- ✅ High compression (10x-100x)
- ✅ Parallel query execution
- ✅ Designed for time-series data
- ❌ No JOINs optimization
- ❌ Eventually consistent

### 1.3 Data Flow

```
Blockchain → Indexer → PostgreSQL → API → User
                  ↓
             ClickHouse → Analytics → Dashboard
```

**Strategy**:
1. **Indexer** writes to PostgreSQL (source of truth)
2. **Async pipeline** copies to ClickHouse for analytics
3. **API** reads from PostgreSQL (latest data)
4. **Analytics** queries ClickHouse (historical trends)

---

## PostgreSQL Schema Design

### 2.1 Core Tables

#### Blocks Table

```sql
-- blocks table: Store blockchain blocks
CREATE TABLE blocks (
    -- Primary key
    block_number BIGINT PRIMARY KEY,

    -- Block identification
    block_hash VARCHAR(66) NOT NULL UNIQUE,
    parent_hash VARCHAR(66) NOT NULL,

    -- Timestamps
    timestamp BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Block metadata
    miner VARCHAR(42) NOT NULL,
    difficulty NUMERIC(78, 0),
    total_difficulty NUMERIC(78, 0),
    size BIGINT,
    gas_limit BIGINT NOT NULL,
    gas_used BIGINT NOT NULL,
    base_fee_per_gas BIGINT,

    -- Transaction data
    transaction_count INT NOT NULL DEFAULT 0,

    -- Consensus data
    nonce VARCHAR(18),
    extra_data TEXT,

    -- State
    state_root VARCHAR(66),
    transactions_root VARCHAR(66),
    receipts_root VARCHAR(66),

    -- Indexing metadata
    indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_reorged BOOLEAN DEFAULT FALSE
);

-- Indexes
CREATE INDEX idx_blocks_timestamp ON blocks (timestamp DESC);
CREATE INDEX idx_blocks_miner ON blocks (miner);
CREATE INDEX idx_blocks_hash ON blocks (block_hash);
CREATE INDEX idx_blocks_indexed_at ON blocks (indexed_at DESC);

-- Comment
COMMENT ON TABLE blocks IS 'Ethereum blockchain blocks';
COMMENT ON COLUMN blocks.block_number IS 'Block height (sequential)';
COMMENT ON COLUMN blocks.block_hash IS 'Unique block hash (0x...)';
COMMENT ON COLUMN blocks.base_fee_per_gas IS 'EIP-1559 base fee (wei)';
```

#### Transactions Table

```sql
-- transactions table: Store blockchain transactions
CREATE TABLE transactions (
    -- Primary key
    transaction_hash VARCHAR(66) PRIMARY KEY,

    -- Block reference
    block_number BIGINT NOT NULL REFERENCES blocks(block_number) ON DELETE CASCADE,
    block_hash VARCHAR(66) NOT NULL,
    transaction_index INT NOT NULL,

    -- Transaction metadata
    timestamp BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Addresses
    from_address VARCHAR(42) NOT NULL,
    to_address VARCHAR(42),  -- NULL for contract creation
    contract_address VARCHAR(42),  -- Set if contract creation

    -- Value and gas
    value NUMERIC(78, 0) NOT NULL DEFAULT 0,
    gas_limit BIGINT NOT NULL,
    gas_used BIGINT,
    gas_price BIGINT,
    max_fee_per_gas BIGINT,  -- EIP-1559
    max_priority_fee_per_gas BIGINT,  -- EIP-1559
    effective_gas_price BIGINT,

    -- Transaction data
    input TEXT,
    nonce BIGINT NOT NULL,
    transaction_type INT DEFAULT 0,  -- 0: Legacy, 1: EIP-2930, 2: EIP-1559

    -- Status
    status INT,  -- 1: Success, 0: Failed

    -- Signature
    v VARCHAR(66),
    r VARCHAR(66),
    s VARCHAR(66),

    -- Indexing metadata
    indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_reorged BOOLEAN DEFAULT FALSE,

    -- Constraints
    UNIQUE (block_number, transaction_index)
);

-- Indexes
CREATE INDEX idx_transactions_block_number ON transactions (block_number DESC);
CREATE INDEX idx_transactions_from_address ON transactions (from_address);
CREATE INDEX idx_transactions_to_address ON transactions (to_address) WHERE to_address IS NOT NULL;
CREATE INDEX idx_transactions_contract_address ON transactions (contract_address) WHERE contract_address IS NOT NULL;
CREATE INDEX idx_transactions_timestamp ON transactions (timestamp DESC);
CREATE INDEX idx_transactions_status ON transactions (status);
CREATE INDEX idx_transactions_value ON transactions (value DESC) WHERE value > 0;

-- Partial index for contract creations
CREATE INDEX idx_transactions_contract_creation ON transactions (from_address, block_number DESC)
WHERE to_address IS NULL;

-- Comment
COMMENT ON TABLE transactions IS 'Ethereum transactions';
COMMENT ON COLUMN transactions.to_address IS 'Recipient address (NULL for contract creation)';
COMMENT ON COLUMN transactions.contract_address IS 'Created contract address (if applicable)';
```

#### Logs (Events) Table

```sql
-- logs table: Store event logs emitted by smart contracts
CREATE TABLE logs (
    -- Primary key (composite)
    id BIGSERIAL PRIMARY KEY,

    -- Transaction reference
    transaction_hash VARCHAR(66) NOT NULL REFERENCES transactions(transaction_hash) ON DELETE CASCADE,
    block_number BIGINT NOT NULL REFERENCES blocks(block_number) ON DELETE CASCADE,
    block_hash VARCHAR(66) NOT NULL,

    -- Log metadata
    log_index INT NOT NULL,
    timestamp BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Contract that emitted the log
    address VARCHAR(42) NOT NULL,

    -- Topics (indexed event parameters)
    topic0 VARCHAR(66),  -- Event signature hash
    topic1 VARCHAR(66),
    topic2 VARCHAR(66),
    topic3 VARCHAR(66),

    -- Non-indexed data
    data TEXT,

    -- Indexing metadata
    indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_reorged BOOLEAN DEFAULT FALSE,

    -- Constraints
    UNIQUE (transaction_hash, log_index)
);

-- Indexes
CREATE INDEX idx_logs_block_number ON logs (block_number DESC);
CREATE INDEX idx_logs_transaction_hash ON logs (transaction_hash);
CREATE INDEX idx_logs_address ON logs (address);
CREATE INDEX idx_logs_topic0 ON logs (topic0) WHERE topic0 IS NOT NULL;
CREATE INDEX idx_logs_topic1 ON logs (topic1) WHERE topic1 IS NOT NULL;
CREATE INDEX idx_logs_topic2 ON logs (topic2) WHERE topic2 IS NOT NULL;
CREATE INDEX idx_logs_topic3 ON logs (topic3) WHERE topic3 IS NOT NULL;
CREATE INDEX idx_logs_timestamp ON logs (timestamp DESC);

-- Composite index for common queries
CREATE INDEX idx_logs_address_topic0 ON logs (address, topic0) WHERE topic0 IS NOT NULL;

-- Comment
COMMENT ON TABLE logs IS 'Smart contract event logs';
COMMENT ON COLUMN logs.topic0 IS 'Event signature (keccak256 of event definition)';
COMMENT ON COLUMN logs.data IS 'ABI-encoded non-indexed parameters';
```

#### Addresses Table

```sql
-- addresses table: Track address metadata and statistics
CREATE TABLE addresses (
    -- Primary key
    address VARCHAR(42) PRIMARY KEY,

    -- Address type
    is_contract BOOLEAN DEFAULT FALSE,
    is_token BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,

    -- Contract metadata (if applicable)
    contract_creator VARCHAR(42),
    contract_created_at_block BIGINT,
    contract_created_at_tx VARCHAR(66),

    -- Statistics (cached)
    balance NUMERIC(78, 0) DEFAULT 0,
    transaction_count BIGINT DEFAULT 0,
    token_transfer_count BIGINT DEFAULT 0,

    -- Labels and metadata
    name VARCHAR(255),
    symbol VARCHAR(50),
    label VARCHAR(255),  -- e.g., "Binance Hot Wallet"
    tags TEXT[],  -- e.g., ['exchange', 'hot-wallet']

    -- Timestamps
    first_seen_at BIGINT,
    last_seen_at BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_addresses_is_contract ON addresses (is_contract) WHERE is_contract = TRUE;
CREATE INDEX idx_addresses_is_token ON addresses (is_token) WHERE is_token = TRUE;
CREATE INDEX idx_addresses_transaction_count ON addresses (transaction_count DESC);
CREATE INDEX idx_addresses_name ON addresses USING gin (name gin_trgm_ops);  -- Full-text search

-- Comment
COMMENT ON TABLE addresses IS 'Address metadata and statistics';
COMMENT ON COLUMN addresses.tags IS 'Array of tags for categorization';
```

#### Tokens Table

```sql
-- tokens table: Store ERC-20/721/1155 token information
CREATE TABLE tokens (
    -- Primary key
    address VARCHAR(42) PRIMARY KEY REFERENCES addresses(address),

    -- Token standard
    token_type VARCHAR(10) NOT NULL,  -- 'ERC20', 'ERC721', 'ERC1155'

    -- Token metadata
    name VARCHAR(255),
    symbol VARCHAR(50),
    decimals INT,
    total_supply NUMERIC(78, 0),

    -- Contract info
    creator VARCHAR(42),
    created_at_block BIGINT,
    created_at_tx VARCHAR(66),

    -- Statistics
    holder_count BIGINT DEFAULT 0,
    transfer_count BIGINT DEFAULT 0,

    -- Metadata
    icon_url TEXT,
    website TEXT,
    description TEXT,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_tokens_token_type ON tokens (token_type);
CREATE INDEX idx_tokens_holder_count ON tokens (holder_count DESC);
CREATE INDEX idx_tokens_transfer_count ON tokens (transfer_count DESC);
CREATE INDEX idx_tokens_symbol ON tokens (symbol);

-- Comment
COMMENT ON TABLE tokens IS 'ERC token contracts metadata';
```

#### Token Transfers Table

```sql
-- token_transfers table: Store ERC-20/721/1155 transfer events
CREATE TABLE token_transfers (
    -- Primary key
    id BIGSERIAL PRIMARY KEY,

    -- References
    transaction_hash VARCHAR(66) NOT NULL REFERENCES transactions(transaction_hash) ON DELETE CASCADE,
    log_index INT NOT NULL,
    block_number BIGINT NOT NULL,
    timestamp BIGINT NOT NULL,

    -- Token info
    token_address VARCHAR(42) NOT NULL REFERENCES tokens(address),
    token_type VARCHAR(10) NOT NULL,

    -- Transfer details
    from_address VARCHAR(42) NOT NULL,
    to_address VARCHAR(42) NOT NULL,
    value NUMERIC(78, 0),  -- For ERC-20 and ERC-1155
    token_id NUMERIC(78, 0),  -- For ERC-721 and ERC-1155

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_reorged BOOLEAN DEFAULT FALSE,

    -- Constraints
    UNIQUE (transaction_hash, log_index)
);

-- Indexes
CREATE INDEX idx_token_transfers_block_number ON token_transfers (block_number DESC);
CREATE INDEX idx_token_transfers_token_address ON token_transfers (token_address);
CREATE INDEX idx_token_transfers_from_address ON token_transfers (from_address);
CREATE INDEX idx_token_transfers_to_address ON token_transfers (to_address);
CREATE INDEX idx_token_transfers_timestamp ON token_transfers (timestamp DESC);
CREATE INDEX idx_token_transfers_token_id ON token_transfers (token_address, token_id) WHERE token_id IS NOT NULL;

-- Comment
COMMENT ON TABLE token_transfers IS 'ERC token transfer events';
```

### 2.2 Supporting Tables

#### Indexer State Table

```sql
-- indexer_state table: Track indexer progress
CREATE TABLE indexer_state (
    id INT PRIMARY KEY DEFAULT 1,
    last_indexed_block BIGINT NOT NULL DEFAULT 0,
    last_indexed_block_hash VARCHAR(66),
    last_indexed_timestamp BIGINT,
    indexer_version VARCHAR(50),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Ensure single row
    CONSTRAINT single_row CHECK (id = 1)
);

-- Insert initial state
INSERT INTO indexer_state (id, last_indexed_block) VALUES (1, 0);

COMMENT ON TABLE indexer_state IS 'Indexer checkpoint and state';
```

#### Reorg History Table

```sql
-- reorg_history table: Track blockchain reorganizations
CREATE TABLE reorg_history (
    id SERIAL PRIMARY KEY,

    -- Reorg details
    detected_at_block BIGINT NOT NULL,
    reorg_depth INT NOT NULL,
    old_block_hash VARCHAR(66) NOT NULL,
    new_block_hash VARCHAR(66) NOT NULL,

    -- Affected data
    blocks_affected INT,
    transactions_affected INT,
    logs_affected INT,

    -- Timestamps
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP
);

CREATE INDEX idx_reorg_history_detected_at ON reorg_history (detected_at DESC);

COMMENT ON TABLE reorg_history IS 'Blockchain reorganization history';
```

### 2.3 Schema Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                     Schema Relationships                    │
└─────────────────────────────────────────────────────────────┘

blocks (1) ──┬──► (N) transactions
             │
             └──► (N) logs

transactions (1) ──┬──► (N) logs
                   │
                   └──► (N) token_transfers

addresses (1) ◄──── (N) transactions (from_address, to_address)
addresses (1) ◄──── (N) token_transfers (from_address, to_address)
addresses (1) ◄──── (1) tokens (address)

tokens (1) ◄──── (N) token_transfers (token_address)
```

---

## ClickHouse Analytics Schema

### 3.1 Why ClickHouse?

**Performance comparison** (1B rows):

```
┌────────────────────────┬──────────────┬──────────────┐
│ Query Type             │ PostgreSQL   │ ClickHouse   │
├────────────────────────┼──────────────┼──────────────┤
│ COUNT(*)               │ 45s          │ 0.2s         │
│ SUM(value) GROUP BY    │ 120s         │ 1.5s         │
│ Daily aggregations     │ 300s         │ 3s           │
│ Storage size           │ 500GB        │ 50GB         │
└────────────────────────┴──────────────┴──────────────┘
```

### 3.2 Fact Tables

#### fact_transactions

```sql
-- fact_transactions: Optimized for analytics
CREATE TABLE fact_transactions (
    -- Identifiers
    transaction_hash String,
    block_number UInt64,
    transaction_index UInt32,

    -- Timestamp (partitioning key)
    timestamp UInt64,
    date Date,
    hour DateTime,

    -- Addresses
    from_address String,
    to_address String,

    -- Value and gas
    value UInt256,
    gas_limit UInt64,
    gas_used UInt64,
    gas_price UInt64,
    effective_gas_price UInt64,
    transaction_fee UInt128,  -- gas_used * effective_gas_price

    -- Transaction type
    transaction_type UInt8,
    status UInt8,
    is_contract_creation UInt8,

    -- Metadata
    input_size UInt32,  -- LENGTH(input)

    -- Indexing
    indexed_at DateTime DEFAULT now()
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (date, block_number, transaction_index)
SETTINGS index_granularity = 8192;

-- Secondary indexes
CREATE INDEX idx_from_address ON fact_transactions (from_address) TYPE bloom_filter GRANULARITY 1;
CREATE INDEX idx_to_address ON fact_transactions (to_address) TYPE bloom_filter GRANULARITY 1;

COMMENT ON TABLE fact_transactions 'Transaction analytics fact table';
```

#### fact_logs

```sql
-- fact_logs: Event logs for analytics
CREATE TABLE fact_logs (
    -- Identifiers
    transaction_hash String,
    log_index UInt32,
    block_number UInt64,

    -- Timestamp
    timestamp UInt64,
    date Date,
    hour DateTime,

    -- Contract
    address String,

    -- Topics
    topic0 String,
    topic1 String,
    topic2 String,
    topic3 String,

    -- Data
    data_size UInt32,

    -- Indexing
    indexed_at DateTime DEFAULT now()
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (date, address, topic0, block_number, log_index)
SETTINGS index_granularity = 8192;

-- Indexes
CREATE INDEX idx_address ON fact_logs (address) TYPE bloom_filter GRANULARITY 1;
CREATE INDEX idx_topic0 ON fact_logs (topic0) TYPE bloom_filter GRANULARITY 1;

COMMENT ON TABLE fact_logs 'Event logs analytics fact table';
```

#### fact_token_transfers

```sql
-- fact_token_transfers: Token transfer analytics
CREATE TABLE fact_token_transfers (
    -- Identifiers
    transaction_hash String,
    log_index UInt32,
    block_number UInt64,

    -- Timestamp
    timestamp UInt64,
    date Date,
    hour DateTime,

    -- Token
    token_address String,
    token_type String,

    -- Transfer
    from_address String,
    to_address String,
    value UInt256,
    token_id Nullable(UInt256),

    -- Indexing
    indexed_at DateTime DEFAULT now()
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (date, token_address, block_number, log_index)
SETTINGS index_granularity = 8192;

-- Indexes
CREATE INDEX idx_token_address ON fact_token_transfers (token_address) TYPE bloom_filter GRANULARITY 1;
CREATE INDEX idx_from ON fact_token_transfers (from_address) TYPE bloom_filter GRANULARITY 1;
CREATE INDEX idx_to ON fact_token_transfers (to_address) TYPE bloom_filter GRANULARITY 1;

COMMENT ON TABLE fact_token_transfers 'Token transfer analytics';
```

### 3.3 Aggregation Tables

#### agg_daily_stats

```sql
-- agg_daily_stats: Daily blockchain statistics
CREATE TABLE agg_daily_stats (
    date Date,

    -- Block stats
    block_count UInt32,
    avg_block_size Float64,
    avg_block_time Float64,

    -- Transaction stats
    transaction_count UInt64,
    unique_addresses UInt64,
    avg_gas_price Float64,
    total_gas_used UInt128,
    total_transaction_fees UInt256,

    -- Value transfers
    total_value_transferred UInt256,
    avg_transaction_value Float64,

    -- Contract stats
    contract_creations UInt32,
    contract_calls UInt64,

    -- Token stats
    token_transfers UInt64,
    unique_token_senders UInt64,
    unique_token_receivers UInt64,

    -- Computed at
    computed_at DateTime DEFAULT now()
)
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (date)
SETTINGS index_granularity = 8192;

COMMENT ON TABLE agg_daily_stats 'Daily aggregated blockchain statistics';
```

#### agg_hourly_gas

```sql
-- agg_hourly_gas: Hourly gas statistics
CREATE TABLE agg_hourly_gas (
    hour DateTime,

    -- Gas metrics
    min_gas_price UInt64,
    max_gas_price UInt64,
    avg_gas_price Float64,
    median_gas_price UInt64,
    p95_gas_price UInt64,

    -- Transaction count
    transaction_count UInt64,

    -- Total gas
    total_gas_used UInt128,

    -- Computed at
    computed_at DateTime DEFAULT now()
)
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(toDate(hour))
ORDER BY (hour)
SETTINGS index_granularity = 8192;

COMMENT ON TABLE agg_hourly_gas 'Hourly gas price statistics';
```

### 3.4 Materialized Views

#### mv_daily_stats

```sql
-- Materialized view: Auto-compute daily stats
CREATE MATERIALIZED VIEW mv_daily_stats TO agg_daily_stats AS
SELECT
    date,
    COUNT(DISTINCT block_number) AS block_count,
    AVG(input_size) AS avg_block_size,
    0 AS avg_block_time,  -- Computed separately
    COUNT(*) AS transaction_count,
    uniq(from_address) + uniq(to_address) AS unique_addresses,
    AVG(gas_price) AS avg_gas_price,
    SUM(gas_used) AS total_gas_used,
    SUM(transaction_fee) AS total_transaction_fees,
    SUM(value) AS total_value_transferred,
    AVG(value) AS avg_transaction_value,
    sumIf(1, is_contract_creation = 1) AS contract_creations,
    sumIf(1, is_contract_creation = 0) AS contract_calls,
    0 AS token_transfers,
    0 AS unique_token_senders,
    0 AS unique_token_receivers,
    now() AS computed_at
FROM fact_transactions
GROUP BY date;
```

#### mv_hourly_gas

```sql
-- Materialized view: Auto-compute hourly gas stats
CREATE MATERIALIZED VIEW mv_hourly_gas TO agg_hourly_gas AS
SELECT
    toStartOfHour(hour) AS hour,
    min(gas_price) AS min_gas_price,
    max(gas_price) AS max_gas_price,
    avg(gas_price) AS avg_gas_price,
    quantile(0.5)(gas_price) AS median_gas_price,
    quantile(0.95)(gas_price) AS p95_gas_price,
    COUNT(*) AS transaction_count,
    SUM(gas_used) AS total_gas_used,
    now() AS computed_at
FROM fact_transactions
GROUP BY hour;
```

---

## Indexing Strategy

### 4.1 PostgreSQL Index Types

#### B-Tree Index (Default)

```sql
-- Good for: =, <, >, <=, >=, BETWEEN, ORDER BY
CREATE INDEX idx_blocks_number ON blocks (block_number);
CREATE INDEX idx_transactions_timestamp ON transactions (timestamp DESC);

-- Composite index (left-to-right matching)
CREATE INDEX idx_logs_address_topic0 ON logs (address, topic0);
-- Can use for:
--   WHERE address = ? AND topic0 = ?  ✅
--   WHERE address = ?                 ✅
--   WHERE topic0 = ?                  ❌ (won't use index)
```

#### GIN Index (Generalized Inverted Index)

```sql
-- Good for: Full-text search, array operations, JSONB
-- Enable extension
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Full-text search on address names
CREATE INDEX idx_addresses_name_gin ON addresses USING gin (name gin_trgm_ops);

-- Array containment
CREATE INDEX idx_addresses_tags_gin ON addresses USING gin (tags);

-- Query examples:
-- Full-text: SELECT * FROM addresses WHERE name ILIKE '%binance%';
-- Array: SELECT * FROM addresses WHERE 'exchange' = ANY(tags);
```

#### Partial Index

```sql
-- Index only subset of rows (saves space, faster)
CREATE INDEX idx_transactions_contract_creation
ON transactions (from_address, block_number DESC)
WHERE to_address IS NULL;

CREATE INDEX idx_addresses_contracts
ON addresses (address)
WHERE is_contract = TRUE;

CREATE INDEX idx_transactions_failed
ON transactions (block_number DESC)
WHERE status = 0;
```

#### Covering Index (Index-Only Scan)

```sql
-- Include extra columns in index leaf nodes
CREATE INDEX idx_transactions_from_covering
ON transactions (from_address)
INCLUDE (block_number, value, gas_used);

-- Query can be satisfied from index alone (no table scan)
-- SELECT block_number, value, gas_used FROM transactions WHERE from_address = ?;
```

### 4.2 Index Best Practices

**DO**:
- ✅ Index foreign keys
- ✅ Index columns used in WHERE, JOIN, ORDER BY
- ✅ Use partial indexes for filtered queries
- ✅ Monitor index usage (`pg_stat_user_indexes`)
- ✅ Create indexes CONCURRENTLY in production

**DON'T**:
- ❌ Over-index (slows down writes, wastes space)
- ❌ Index low-cardinality columns (e.g., boolean) unless partial
- ❌ Index columns with high write frequency
- ❌ Forget to ANALYZE after bulk inserts

### 4.3 Index Maintenance

```sql
-- Check index usage
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;

-- Find unused indexes (idx_scan = 0)
SELECT
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexname NOT LIKE 'pg_toast%';

-- Reindex (rebuilds index, can fix bloat)
REINDEX INDEX CONCURRENTLY idx_transactions_block_number;

-- Vacuum analyze (updates statistics)
VACUUM ANALYZE transactions;
```

---

## Migrations with Alembic

### 5.1 Alembic Setup

```bash
# Install Alembic
pip install alembic psycopg2-binary

# Initialize Alembic
alembic init alembic

# Directory structure
alembic/
├── env.py              # Migration environment
├── script.py.mako      # Migration template
├── versions/           # Migration files
└── alembic.ini         # Configuration
```

### 5.2 Configuration

**alembic.ini**:

```ini
[alembic]
script_location = alembic
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d_%%(rev)s_%%(slug)s

# Database URL (can use env var)
sqlalchemy.url = postgresql://user:password@localhost:5432/blockchain_explorer

# Logging
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

**env.py** (with async support):

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os

# Import your models
from app.models import Base

# Alembic Config object
config = context.config

# Override sqlalchemy.url with environment variable
if os.getenv("DATABASE_URL"):
    config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Detect column type changes
            compare_server_default=True,  # Detect default value changes
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 5.3 Creating Migrations

```bash
# Auto-generate migration from models
alembic revision --autogenerate -m "create blocks and transactions tables"

# Create empty migration (manual)
alembic revision -m "add custom index"

# Migration file: alembic/versions/20250106_1430_a1b2c3d4e5f6_create_blocks_table.py
```

**Example migration**:

```python
"""create blocks and transactions tables

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2025-01-06 14:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'a1b2c3d4e5f6'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create blocks table
    op.create_table(
        'blocks',
        sa.Column('block_number', sa.BigInteger(), nullable=False),
        sa.Column('block_hash', sa.String(length=66), nullable=False),
        sa.Column('parent_hash', sa.String(length=66), nullable=False),
        sa.Column('timestamp', sa.BigInteger(), nullable=False),
        sa.Column('miner', sa.String(length=42), nullable=False),
        sa.Column('difficulty', sa.Numeric(precision=78, scale=0), nullable=True),
        sa.Column('total_difficulty', sa.Numeric(precision=78, scale=0), nullable=True),
        sa.Column('size', sa.BigInteger(), nullable=True),
        sa.Column('gas_limit', sa.BigInteger(), nullable=False),
        sa.Column('gas_used', sa.BigInteger(), nullable=False),
        sa.Column('base_fee_per_gas', sa.BigInteger(), nullable=True),
        sa.Column('transaction_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('indexed_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('is_reorged', sa.Boolean(), server_default='false'),
        sa.PrimaryKeyConstraint('block_number'),
        sa.UniqueConstraint('block_hash')
    )

    # Create indexes
    op.create_index('idx_blocks_timestamp', 'blocks', ['timestamp'], unique=False)
    op.create_index('idx_blocks_miner', 'blocks', ['miner'], unique=False)
    op.create_index('idx_blocks_hash', 'blocks', ['block_hash'], unique=False)

    # Create transactions table
    op.create_table(
        'transactions',
        sa.Column('transaction_hash', sa.String(length=66), nullable=False),
        sa.Column('block_number', sa.BigInteger(), nullable=False),
        sa.Column('block_hash', sa.String(length=66), nullable=False),
        sa.Column('transaction_index', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.BigInteger(), nullable=False),
        sa.Column('from_address', sa.String(length=42), nullable=False),
        sa.Column('to_address', sa.String(length=42), nullable=True),
        sa.Column('value', sa.Numeric(precision=78, scale=0), nullable=False, server_default='0'),
        sa.Column('gas_limit', sa.BigInteger(), nullable=False),
        sa.Column('gas_used', sa.BigInteger(), nullable=True),
        sa.Column('gas_price', sa.BigInteger(), nullable=True),
        sa.Column('status', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('indexed_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('is_reorged', sa.Boolean(), server_default='false'),
        sa.ForeignKeyConstraint(['block_number'], ['blocks.block_number'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('transaction_hash'),
        sa.UniqueConstraint('block_number', 'transaction_index')
    )

    # Create indexes
    op.create_index('idx_transactions_block_number', 'transactions', ['block_number'], unique=False)
    op.create_index('idx_transactions_from_address', 'transactions', ['from_address'], unique=False)
    op.create_index('idx_transactions_to_address', 'transactions', ['to_address'], unique=False)

def downgrade() -> None:
    op.drop_table('transactions')
    op.drop_table('blocks')
```

### 5.4 Running Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Downgrade one version
alembic downgrade -1

# Show current version
alembic current

# Show migration history
alembic history --verbose

# Stamp database (mark as migrated without running)
alembic stamp head

# Dry run (show SQL without executing)
alembic upgrade head --sql
```

### 5.5 Migration Best Practices

**DO**:
- ✅ Review auto-generated migrations (they're not perfect)
- ✅ Test migrations on staging first
- ✅ Create indexes CONCURRENTLY (no table lock)
- ✅ Add NOT NULL constraints in multiple steps
- ✅ Batch large data migrations
- ✅ Keep migrations small and focused

**Example: Add NOT NULL constraint safely**:

```python
# Migration 1: Add column (nullable)
def upgrade():
    op.add_column('transactions', sa.Column('effective_gas_price', sa.BigInteger(), nullable=True))

# Migration 2: Backfill data
def upgrade():
    op.execute("""
        UPDATE transactions
        SET effective_gas_price = gas_price
        WHERE effective_gas_price IS NULL
    """)

# Migration 3: Add NOT NULL constraint
def upgrade():
    op.alter_column('transactions', 'effective_gas_price', nullable=False)
```

---

## Query Optimization

### 6.1 Common Query Patterns

#### Get latest blocks

```sql
-- Bad: Full table scan
SELECT * FROM blocks ORDER BY block_number DESC LIMIT 10;

-- Good: Uses index on block_number
SELECT * FROM blocks ORDER BY block_number DESC LIMIT 10;
-- Index: CREATE INDEX idx_blocks_number_desc ON blocks (block_number DESC);
```

#### Get address transactions

```sql
-- Bad: OR condition (can't use single index efficiently)
SELECT * FROM transactions
WHERE from_address = '0x...' OR to_address = '0x...'
ORDER BY block_number DESC
LIMIT 100;

-- Good: UNION ALL (uses both indexes)
(SELECT * FROM transactions WHERE from_address = '0x...' ORDER BY block_number DESC LIMIT 100)
UNION ALL
(SELECT * FROM transactions WHERE to_address = '0x...' AND from_address != '0x...' ORDER BY block_number DESC LIMIT 100)
ORDER BY block_number DESC
LIMIT 100;
```

#### Get token transfers for address

```sql
-- Bad: No index on (from_address, timestamp)
SELECT * FROM token_transfers
WHERE from_address = '0x...'
ORDER BY timestamp DESC
LIMIT 50;

-- Good: Composite index
-- CREATE INDEX idx_token_transfers_from_timestamp ON token_transfers (from_address, timestamp DESC);
```

### 6.2 Query Profiling

```sql
-- Enable timing
\timing on

-- Explain query
EXPLAIN SELECT * FROM transactions WHERE from_address = '0x...';

-- Explain analyze (actually runs query)
EXPLAIN ANALYZE SELECT * FROM transactions WHERE from_address = '0x...';

-- Output:
-- Index Scan using idx_transactions_from_address on transactions  (cost=0.56..8.58 rows=1 width=500) (actual time=0.012..0.013 rows=1 loops=1)
--   Index Cond: ((from_address)::text = '0x...'::text)
-- Planning Time: 0.123 ms
-- Execution Time: 0.045 ms
```

**Reading EXPLAIN output**:

```
┌──────────────────────────────────────────────────────────────┐
│ Scan Type        │ Performance │ Description                 │
├──────────────────────────────────────────────────────────────┤
│ Index Scan       │ ⚡⚡⚡       │ Uses index, very fast       │
│ Index Only Scan  │ ⚡⚡⚡⚡     │ Index covers all columns    │
│ Bitmap Index     │ ⚡⚡         │ Multiple indexes combined   │
│ Seq Scan         │ 🐢          │ Full table scan, slow       │
└──────────────────────────────────────────────────────────────┘
```

### 6.3 Pagination

```sql
-- Bad: OFFSET (slow for large offsets)
SELECT * FROM transactions ORDER BY block_number DESC LIMIT 50 OFFSET 10000;
-- Problem: Scans and discards 10,000 rows

-- Good: Keyset pagination (cursor-based)
SELECT * FROM transactions
WHERE block_number < :last_block_number
ORDER BY block_number DESC
LIMIT 50;
-- Fast: Uses index directly
```

---

## แบบฝึกหัด

### แบบฝึกหัดที่ 1: Create Database Schema

**เป้าหมาย**: สร้าง PostgreSQL schema ตามที่กำหนด

**Requirements**:
- สร้าง tables: blocks, transactions, logs
- เพิ่ม indexes ที่จำเป็น
- ใส่ sample data (10 blocks, 50 transactions, 20 logs)

**Pass criteria**:
- ✅ Schema created successfully
- ✅ Foreign keys work
- ✅ Indexes created
- ✅ Can query sample data

### แบบฝึกหัดที่ 2: Write Alembic Migrations

**เป้าหมาย**: สร้าง migration script

**Requirements**:
- Initialize Alembic
- Auto-generate migration from models
- Add custom index migration
- Apply and rollback migrations

**Pass criteria**:
- ✅ Migrations run without errors
- ✅ Can upgrade and downgrade
- ✅ Schema matches models

### แบบฝึกหัดที่ 3: Query Optimization

**เป้าหมาย**: Optimize slow query

**Given**: This query takes 30 seconds
```sql
SELECT * FROM transactions
WHERE from_address = '0x...' OR to_address = '0x...'
ORDER BY timestamp DESC
LIMIT 100;
```

**Requirements**:
- Rewrite query to use indexes
- Add necessary indexes
- Reduce execution time to < 100ms

**Pass criteria**:
- ✅ Query uses indexes (check EXPLAIN)
- ✅ Execution time < 100ms
- ✅ Returns same results

### แบบฝึกหัดที่ 4: ClickHouse Setup

**เป้าหมาย**: Setup ClickHouse analytics

**Requirements**:
- Create fact_transactions table
- Create materialized view for daily stats
- Insert sample data
- Run aggregation query

**Expected output**:
```sql
SELECT date, COUNT(*) as tx_count, SUM(value) as total_value
FROM fact_transactions
GROUP BY date
ORDER BY date DESC
LIMIT 7;
```

**Pass criteria**:
- ✅ ClickHouse tables created
- ✅ Materialized view works
- ✅ Query returns results in < 1s

### แบบฝึกหัดที่ 5: Data Consistency Check

**เป้าหมาย**: เขียน SQL queries เพื่อตรวจสอบ data quality

**Requirements**:
- Check for missing blocks
- Check for orphaned transactions
- Check for duplicate transaction hashes
- Check for negative gas values

**Example**:
```sql
-- Missing blocks
SELECT block_number + 1 AS missing_block
FROM blocks b1
WHERE NOT EXISTS (
    SELECT 1 FROM blocks b2 WHERE b2.block_number = b1.block_number + 1
)
AND block_number < (SELECT MAX(block_number) FROM blocks);
```

**Pass criteria**:
- ✅ All checks implemented
- ✅ Queries are efficient
- ✅ Found and documented any issues

---

## Pass Criteria - PART04

ก่อนจบ PART04 ให้ตรวจสอบว่า:

- [ ] เข้าใจ dual database architecture (PostgreSQL + ClickHouse)
- [ ] สามารถออกแบบ PostgreSQL schema ได้
- [ ] เข้าใจ foreign keys และ relationships
- [ ] รู้จัก index types และ use cases
- [ ] สามารถใช้ Alembic สร้าง migrations ได้
- [ ] เข้าใจ ClickHouse column-oriented storage
- [ ] รู้จัก MergeTree engine และ partitioning
- [ ] สามารถเขียน query optimization ได้
- [ ] สามารถทำแบบฝึกหัดอย่างน้อย 3 ข้อให้สำเร็จ

---

## Production Notes

### Performance Benchmarks

**PostgreSQL**:
- Insert rate: 5,000-10,000 tx/sec (batched)
- Query latency: < 50ms (p95) with proper indexes
- Connection pool: 20-50 connections
- Vacuum: Auto-vacuum enabled, manual vacuum weekly

**ClickHouse**:
- Insert rate: 100,000+ events/sec
- Query latency: < 1s for billion-row aggregations
- Compression: 10x-100x
- Partitions: Monthly (drop old partitions easily)

### Scalability

**PostgreSQL scaling**:
- Vertical: 64GB RAM, NVMe SSD
- Read replicas: 2-3 replicas for read scaling
- Partitioning: Partition by month (declarative partitioning)
- Connection pooling: PgBouncer

**ClickHouse scaling**:
- Horizontal: Add more shards
- Replication: 2-3 replicas per shard
- Distributed tables: Query across shards
- Retention: Drop old partitions

### Backup Strategy

```bash
# PostgreSQL backup
pg_dump -h localhost -U user -d blockchain_explorer -F c -f backup.dump

# Restore
pg_restore -h localhost -U user -d blockchain_explorer backup.dump

# ClickHouse backup
clickhouse-client --query "BACKUP TABLE fact_transactions TO Disk('backups', 'backup.zip')"
```

### Monitoring Queries

```sql
-- PostgreSQL: Check table sizes
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS table_size,
    pg_size_pretty(pg_indexes_size(schemaname||'.'||tablename)) AS indexes_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- PostgreSQL: Check index bloat
SELECT
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;

-- ClickHouse: Check table sizes
SELECT
    table,
    formatReadableSize(sum(bytes)) AS size,
    sum(rows) AS rows,
    max(modification_time) AS latest_modification
FROM system.parts
WHERE active
GROUP BY table
ORDER BY sum(bytes) DESC;
```

---

## Resources

- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **ClickHouse Docs**: https://clickhouse.com/docs/
- **Alembic Docs**: https://alembic.sqlalchemy.org/
- **Use The Index, Luke**: https://use-the-index-luke.com/
- **PostgreSQL Wiki**: https://wiki.postgresql.org/

---

**จบ PART04 - Database Design & Schema**

**ถัดไป**: PART05 - Indexer & ETL System (Python implementation, reorg handling, performance)

---

**สถิติ PART04**:
- **Lines**: ~1,828 lines
- **Tables**: 10+ complete schemas
- **Queries**: 40+ SQL examples
- **Exercises**: 5 hands-on labs

---

*เอกสารนี้เป็นส่วนหนึ่งของโปรเจกต์ Blockchain Explorer System*
