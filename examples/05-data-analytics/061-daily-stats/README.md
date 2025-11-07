# 061. Blockchain Analytics with ClickHouse

> Production-ready Analytics System for Blockchain Data - 100% Working ✅

## 📋 Overview

A complete analytics pipeline for blockchain data using **ClickHouse** as the analytical database. This project provides:
- **ETL Pipeline**: Extract blockchain data, transform into analytics, load into ClickHouse
- **ClickHouse Schema**: Optimized tables for time-series analytics
- **Analytics API**: FastAPI endpoints to query aggregated data
- **Dashboard**: Pre-built SQL queries and data models

## 🎯 Technologies

- **ClickHouse**: 23.12 (Columnar analytical database)
- **Python**: 3.9+
- **Web3.py**: 6.11+ (Blockchain interaction)
- **FastAPI**: 0.104+ (Analytics API)
- **Docker Compose**: Infrastructure setup
- **clickhouse-driver**: Python client for ClickHouse

## 📊 Level

🔴 **Advanced**

## 💡 Features

### ClickHouse Database
- ✅ Optimized schema with MergeTree engine
- ✅ Partitioning by month for performance
- ✅ Materialized views for fast queries
- ✅ Multiple granularity levels (daily, hourly)
- ✅ Sample data pre-loaded

### ETL Pipeline
- ✅ Extract blocks and transactions from blockchain
- ✅ Transform into aggregated statistics
- ✅ Load into ClickHouse efficiently
- ✅ Support for date ranges
- ✅ Binary search for block-by-timestamp lookup
- ✅ Hourly and daily aggregations

### Analytics Tables
- ✅ `daily_blocks` - Daily block statistics
- ✅ `daily_transactions` - Daily transaction stats
- ✅ `hourly_blocks` - Hourly block metrics
- ✅ `daily_miners` - Top miners per day
- ✅ `hourly_gas_prices` - Gas price trends
- ✅ `network_metrics` - Network activity
- ✅ `contract_deployments` - Contract tracking

### Analytics API
- ✅ Daily block statistics endpoint
- ✅ Daily transaction statistics
- ✅ Hourly granular data
- ✅ Top miners ranking
- ✅ Analytics summary
- ✅ Time-series trends (blocks, gas prices)
- ✅ Health check endpoint

## 🚀 Quick Start

### 1. Prerequisites

```bash
# Docker & Docker Compose installed
docker --version
docker-compose --version

# Python 3.9+
python --version
```

### 2. Installation

```bash
cd examples/05-data-analytics/061-daily-stats

# Install Python dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### 3. Start ClickHouse

```bash
# Start ClickHouse with Docker Compose
docker-compose up -d

# Wait for initialization (about 10 seconds)
# Check logs
docker-compose logs -f clickhouse
```

**Services Available:**
- ClickHouse HTTP: http://localhost:8123
- ClickHouse Native: localhost:9000
- Tabix Web UI: http://localhost:8080

### 4. Verify ClickHouse

```bash
# Test connection
curl http://localhost:8123/ping

# Query sample data
curl -G http://localhost:8123 --data-urlencode "query=SELECT * FROM blockchain_analytics.daily_blocks LIMIT 5"
```

### 5. Run ETL Pipeline

```bash
# Process today's data
python etl/blockchain_etl.py today

# Process yesterday's data
python etl/blockchain_etl.py yesterday

# Process specific date
python etl/blockchain_etl.py 2024-01-15

# Process date range
python etl/blockchain_etl.py 2024-01-01 2024-01-31
```

### 6. Start Analytics API

```bash
# Start API server
uvicorn api.analytics_api:app --host 0.0.0.0 --port 8001 --reload

# API will be available at:
# - http://localhost:8001
# - API Docs: http://localhost:8001/docs
```

## 📚 Usage

### Using Makefile (Recommended)

```bash
# View all commands
make help

# Setup project
make setup

# Start ClickHouse
make start-clickhouse

# Run ETL
make etl-today
make etl-yesterday

# Start API
make api

# Clean everything
make clean
```

### Manual Commands

**ETL Pipeline:**
```bash
# Set environment variables
export RPC_URL=http://localhost:8545
export CLICKHOUSE_HOST=localhost
export CLICKHOUSE_PORT=9000
export CLICKHOUSE_DATABASE=blockchain_analytics

# Run ETL
python etl/blockchain_etl.py today
```

**API Server:**
```bash
# Start with uvicorn
uvicorn api.analytics_api:app --reload

# Or run directly
python api/analytics_api.py
```

## 🗂️ Project Structure

```
061-daily-stats/
├── clickhouse/
│   └── init/
│       └── 01_create_tables.sql      # Database schema (150+ lines)
├── etl/
│   └── blockchain_etl.py             # ETL pipeline (650+ lines)
├── api/
│   └── analytics_api.py              # Analytics API (500+ lines)
├── docker/                            # Docker configs (if needed)
├── docker-compose.yml                # ClickHouse setup
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment template
├── Makefile                           # Convenience commands
└── README.md                          # This file
```

## 📡 API Endpoints

### Base URLs
- **API**: http://localhost:8001
- **Docs**: http://localhost:8001/docs

### Endpoints

#### 1. Health Check
```bash
GET /health

curl http://localhost:8001/health
```

**Response:**
```json
{
  "status": "healthy",
  "clickhouse": "connected",
  "version": "1.0.0"
}
```

#### 2. Daily Block Statistics
```bash
GET /api/analytics/daily/blocks?start_date=2024-01-01&end_date=2024-01-31&limit=30

curl "http://localhost:8001/api/analytics/daily/blocks?limit=7"
```

**Response:**
```json
[
  {
    "date": "2024-01-15",
    "block_count": 7200,
    "avg_block_time": 12.0,
    "min_block_number": 1000000,
    "max_block_number": 1007200,
    "total_transactions": 150000,
    "avg_transactions_per_block": 20.83,
    "total_gas_used": 900000000000,
    "avg_gas_used": 125000000,
    "total_gas_limit": 1080000000000,
    "avg_gas_limit": 150000000,
    "gas_usage_percentage": 83.33,
    "unique_miners": 50
  }
]
```

#### 3. Daily Transaction Statistics
```bash
GET /api/analytics/daily/transactions?start_date=2024-01-01&limit=30

curl "http://localhost:8001/api/analytics/daily/transactions?limit=7"
```

**Response:**
```json
[
  {
    "date": "2024-01-15",
    "transaction_count": 150000,
    "avg_gas_price": 50.5,
    "median_gas_price": 45.0,
    "min_gas_price": 10,
    "max_gas_price": 500,
    "avg_transaction_value": 0.5,
    "total_transaction_value": 75000.0,
    "failed_transactions": 1500,
    "success_rate": 99.0,
    "avg_gas_used": 21000,
    "contract_creations": 250,
    "contract_calls": 30000
  }
]
```

#### 4. Hourly Block Statistics
```bash
GET /api/analytics/hourly/blocks?hours=24

curl "http://localhost:8001/api/analytics/hourly/blocks?hours=24"
```

#### 5. Top Miners
```bash
GET /api/analytics/miners?target_date=2024-01-15&limit=10

curl "http://localhost:8001/api/analytics/miners?limit=10"
```

**Response:**
```json
[
  {
    "date": "2024-01-15",
    "miner": "0x1234...5678",
    "blocks_mined": 150,
    "total_gas_collected": 18750000000,
    "total_transactions": 3000
  }
]
```

#### 6. Analytics Summary
```bash
GET /api/analytics/summary?period=7d

curl "http://localhost:8001/api/analytics/summary?period=30d"
```

**Periods**: `1d`, `7d`, `30d`, `90d`

**Response:**
```json
{
  "period": "7d",
  "total_blocks": 50400,
  "total_transactions": 1050000,
  "avg_block_time": 12.05,
  "avg_gas_price": 51.2,
  "total_value_transferred": 525000.0,
  "unique_miners": 45,
  "avg_gas_usage_pct": 83.1
}
```

#### 7. Time Series Trends
```bash
# Block count trends
GET /api/analytics/trends/blocks?days=30

# Gas price trends
GET /api/analytics/trends/gas?days=30

curl "http://localhost:8001/api/analytics/trends/blocks?days=7"
```

## 🎨 ClickHouse Schema

### Tables Overview

**1. daily_blocks**
- Partitioned by month: `toYYYYMM(date)`
- Ordered by: `date`
- Engine: `MergeTree`

**2. daily_transactions**
- Daily transaction aggregates
- Gas price statistics (avg, median, min, max)
- Success rates and contract interactions

**3. hourly_blocks**
- Hourly granularity for detailed analysis
- Useful for intraday patterns

**4. daily_miners**
- Top miners by blocks mined
- Gas collected and transaction counts

**5. Materialized Views**
- `mv_latest_30days` - Fast 30-day summary
- `mv_hourly_7days` - Hourly data for last 7 days

### Querying ClickHouse Directly

**Via HTTP Interface:**
```bash
# Simple query
curl -G http://localhost:8123 \
  --data-urlencode "query=SELECT COUNT(*) FROM blockchain_analytics.daily_blocks"

# With formatting
curl -G http://localhost:8123 \
  --data-urlencode "query=SELECT * FROM blockchain_analytics.daily_blocks ORDER BY date DESC LIMIT 5 FORMAT Pretty"
```

**Via CLI:**
```bash
# Enter ClickHouse client
docker exec -it blockchain_analytics_clickhouse clickhouse-client

# Run queries
USE blockchain_analytics;
SELECT * FROM daily_blocks ORDER BY date DESC LIMIT 5;

# Aggregate query
SELECT
    date,
    block_count,
    total_transactions,
    gas_usage_percentage
FROM daily_blocks
WHERE date >= today() - 30
ORDER BY date DESC;
```

**Via Tabix Web UI:**
Open http://localhost:8080 in your browser and connect to:
- Host: `clickhouse` (or `localhost`)
- Port: `8123`
- Database: `blockchain_analytics`

## 🔧 Configuration

### Environment Variables

```bash
# .env file
RPC_URL=http://localhost:8545
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=9000
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=
CLICKHOUSE_DATABASE=blockchain_analytics
API_HOST=0.0.0.0
API_PORT=8001
```

### ClickHouse Settings

**docker-compose.yml:**
```yaml
environment:
  CLICKHOUSE_DB: blockchain_analytics
  CLICKHOUSE_USER: analytics_user
  CLICKHOUSE_PASSWORD: analytics_pass
```

### ETL Customization

Edit `etl/blockchain_etl.py`:

```python
# Customize aggregation logic
def transform_daily_blocks(self, blocks: List[Dict]) -> Dict:
    # Add custom metrics here
    pass
```

## 📊 Example Queries

### 1. Daily Block Growth
```sql
SELECT
    date,
    block_count,
    total_transactions,
    gas_usage_percentage
FROM daily_blocks
WHERE date >= today() - 30
ORDER BY date DESC;
```

### 2. Gas Price Trends
```sql
SELECT
    date,
    avg_gas_price,
    median_gas_price,
    max_gas_price
FROM daily_transactions
WHERE date >= today() - 30
ORDER BY date ASC;
```

### 3. Hourly Activity Pattern
```sql
SELECT
    hour,
    AVG(block_count) as avg_blocks,
    AVG(total_transactions) as avg_txs
FROM hourly_blocks
WHERE date >= today() - 7
GROUP BY hour
ORDER BY hour;
```

### 4. Top Miners Last Week
```sql
SELECT
    miner,
    SUM(blocks_mined) as total_blocks,
    SUM(total_gas_collected) as total_gas
FROM daily_miners
WHERE date >= today() - 7
GROUP BY miner
ORDER BY total_blocks DESC
LIMIT 10;
```

### 5. Network Health Metrics
```sql
SELECT
    date,
    avg_block_time,
    avg_transactions_per_block,
    gas_usage_percentage,
    unique_miners
FROM daily_blocks
WHERE date >= today() - 30
ORDER BY date DESC;
```

## 🎓 What You'll Learn

- ✅ ClickHouse columnar database
- ✅ MergeTree engine and partitioning
- ✅ Time-series data modeling
- ✅ ETL pipeline design patterns
- ✅ Blockchain data aggregation
- ✅ Analytical query optimization
- ✅ Materialized views
- ✅ FastAPI for analytics APIs
- ✅ Docker Compose orchestration
- ✅ Binary search algorithms (block lookup)

## ✅ Pass Criteria

1. ✅ ClickHouse starts successfully
2. ✅ Database tables created
3. ✅ Sample data loaded
4. ✅ ETL script runs without errors
5. ✅ Data appears in ClickHouse tables
6. ✅ Analytics API starts successfully
7. ✅ All API endpoints return valid data
8. ✅ Tabix UI can connect to ClickHouse
9. ✅ Queries return results in < 100ms

## 🚀 Next Steps

### 1. Add More Metrics

```python
# In blockchain_etl.py
def transform_token_transfers(self, blocks: List[Dict]) -> List[Dict]:
    """Track ERC-20 token transfers"""
    # Parse event logs for Transfer events
    pass
```

### 2. Create Dashboard

```bash
# Use Grafana with ClickHouse plugin
docker run -d -p 3000:3000 grafana/grafana

# Or build custom dashboard with React + Chart.js
# Connect to analytics API endpoints
```

### 3. Add Real-time Streaming

```python
# Use Kafka + ClickHouse integration
# Stream blocks in real-time instead of batch ETL
```

### 4. Advanced Analytics

```sql
-- Create additional materialized views
CREATE MATERIALIZED VIEW mv_gas_price_percentiles
AS SELECT
    date,
    quantile(0.25)(gas_price) as p25,
    quantile(0.50)(gas_price) as p50,
    quantile(0.75)(gas_price) as p75,
    quantile(0.95)(gas_price) as p95
FROM transactions
GROUP BY date;
```

### 5. Machine Learning

```python
# Export data for ML models
# Predict gas prices, block times, network congestion
import pandas as pd

# Fetch data from API
df = pd.DataFrame(requests.get('http://localhost:8001/api/analytics/daily/blocks').json())

# Train model
from sklearn.linear_model import LinearRegression
# ...
```

## 📚 Related Projects

- **031-block-api**: Blockchain Explorer API (data source)
- **046-block-list**: Blockchain Explorer Frontend
- **071-docker-multistage**: Docker deployment

## 🐛 Troubleshooting

**Problem: ClickHouse won't start**
```bash
# Check logs
docker-compose logs clickhouse

# Ensure ports are free
lsof -i :8123
lsof -i :9000

# Try stopping and restarting
docker-compose down
docker-compose up -d
```

**Problem: ETL can't connect to blockchain**
```bash
# Test RPC connection
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'

# Check .env file
cat .env | grep RPC_URL
```

**Problem: No data in ClickHouse**
```bash
# Verify tables exist
docker exec -it blockchain_analytics_clickhouse clickhouse-client \
  -q "SHOW TABLES FROM blockchain_analytics"

# Check if ETL ran successfully
docker-compose logs clickhouse | grep INSERT

# Run ETL again
python etl/blockchain_etl.py yesterday
```

**Problem: API returns 500 error**
```bash
# Check ClickHouse connection
curl http://localhost:8123/ping

# Test API health
curl http://localhost:8001/health

# Check API logs
# Look for ClickHouse connection errors
```

**Problem: Queries are slow**
```sql
-- Check table sizes
SELECT
    table,
    formatReadableSize(sum(bytes)) as size,
    sum(rows) as rows
FROM system.parts
WHERE database = 'blockchain_analytics'
GROUP BY table;

-- Add indexes if needed
-- Already optimized with MergeTree ORDER BY
```

## 🎯 Performance Tips

1. **Partitioning**: Already done by month
2. **Materialized Views**: Pre-aggregate common queries
3. **Sampling**: Use `SAMPLE 0.1` for large datasets
4. **Indexes**: MergeTree ORDER BY creates sparse index
5. **Compression**: ClickHouse compresses data automatically
6. **Query Optimization**:
   - Filter by partition key (date)
   - Use appropriate data types
   - Avoid SELECT *

## 📖 Additional Resources

- [ClickHouse Documentation](https://clickhouse.com/docs)
- [MergeTree Engine Guide](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree)
- [ClickHouse Python Driver](https://github.com/mymarilyn/clickhouse-driver)
- [Time Series Best Practices](https://clickhouse.com/docs/en/guides/best-practices/)

---

**License**: MIT
**Version**: 1.0.0
**Total Lines**: 1,300+ (Python + SQL)
**Database**: ClickHouse 23.12
**Status**: Production Ready ✅
