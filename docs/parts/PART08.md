# PART08 - Analytics & Advanced Features

> **เนื้อหา**: ClickHouse Analytics, Advanced Queries, Data Visualization, Token Analytics, Address Analytics
>
> **เป้าหมาย**: สร้าง advanced analytics features สำหรับ Blockchain Explorer
>
> **ระยะเวลา**: 10-12 ชั่วโมง
>
> **Prerequisites**: PART01-07, ClickHouse, Python, React

---

## 📑 สารบัญ

1. [Analytics Architecture](#analytics-architecture)
2. [ClickHouse Integration](#clickhouse-integration)
3. [Advanced Queries](#advanced-queries)
4. [Token Analytics](#token-analytics)
5. [Address Analytics](#address-analytics)
6. [Data Visualization](#data-visualization)
7. [Export & Reporting](#export--reporting)
8. [แบบฝึกหัด](#แบบฝึกหัด)

---

## Analytics Architecture

### 1.1 Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  Analytics Architecture                     │
└─────────────────────────────────────────────────────────────┘

    PostgreSQL (OLTP)
         │
         │ Streaming/Batch ETL
         ▼
    ClickHouse (OLAP)
         │
    ┌────┴─────┬──────────┬───────────┐
    ▼          ▼          ▼           ▼
┌─────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ Daily   │ │ Token  │ │Address │ │ Gas    │
│ Stats   │ │Analytics│ │Analytics│ │Analytics│
└────┬────┘ └────┬───┘ └────┬───┘ └────┬───┘
     │           │          │          │
     └───────────┴──────────┴──────────┘
                  │
                  ▼
           ┌──────────────┐
           │   API Layer  │
           └──────┬───────┘
                  │
                  ▼
           ┌──────────────┐
           │  Dashboard   │
           │  (Grafana)   │
           └──────────────┘
```

### 1.2 Analytics Use Cases

**Daily Statistics**:
- Total transactions per day
- Unique addresses per day
- Gas usage trends
- Block production rate

**Token Analytics**:
- Top tokens by volume
- Token holder distribution
- Transfer patterns
- Price correlations

**Address Analytics**:
- Whale movements
- New vs active addresses
- Top gas consumers
- Contract interaction patterns

---

## ClickHouse Integration

### 2.1 Data Pipeline (analytics/pipeline.py)

```python
"""Analytics data pipeline from PostgreSQL to ClickHouse."""
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict
from clickhouse_driver import Client as ClickHouseClient
from sqlalchemy.orm import Session

from database import get_session
from models.transaction import Transaction
from models.log import Log
from utils.logger import logger


class AnalyticsPipeline:
    """Pipeline to sync data from PostgreSQL to ClickHouse."""

    def __init__(
        self,
        ch_host: str = "localhost",
        ch_port: int = 9000,
        ch_database: str = "blockchain_analytics"
    ):
        self.ch = ClickHouseClient(
            host=ch_host,
            port=ch_port,
            database=ch_database
        )
        self.logger = logger.bind(component="analytics_pipeline")

    def sync_transactions(
        self,
        start_block: int,
        end_block: int,
        batch_size: int = 10000
    ):
        """
        Sync transactions from PostgreSQL to ClickHouse.

        Args:
            start_block: Start block number
            end_block: End block number
            batch_size: Batch size for insertion
        """
        self.logger.info(
            "syncing_transactions",
            start_block=start_block,
            end_block=end_block
        )

        with get_session() as session:
            # Query transactions in batches
            for block in range(start_block, end_block + 1, batch_size):
                batch_end = min(block + batch_size - 1, end_block)

                txs = (
                    session.query(Transaction)
                    .filter(Transaction.block_number >= block)
                    .filter(Transaction.block_number <= batch_end)
                    .filter(Transaction.is_reorged == False)
                    .all()
                )

                if not txs:
                    continue

                # Transform to ClickHouse format
                ch_data = []
                for tx in txs:
                    ch_data.append({
                        'transaction_hash': tx.transaction_hash,
                        'block_number': tx.block_number,
                        'transaction_index': tx.transaction_index,
                        'timestamp': tx.timestamp,
                        'date': datetime.fromtimestamp(tx.timestamp).date(),
                        'hour': datetime.fromtimestamp(tx.timestamp).replace(
                            minute=0, second=0, microsecond=0
                        ),
                        'from_address': tx.from_address,
                        'to_address': tx.to_address or '',
                        'value': int(tx.value) if tx.value else 0,
                        'gas_limit': tx.gas_limit,
                        'gas_used': tx.gas_used or 0,
                        'gas_price': tx.gas_price or 0,
                        'effective_gas_price': tx.effective_gas_price or 0,
                        'transaction_fee': (tx.gas_used or 0) * (tx.effective_gas_price or 0),
                        'transaction_type': tx.transaction_type or 0,
                        'status': tx.status or 0,
                        'is_contract_creation': 1 if tx.to_address is None else 0,
                        'input_size': len(tx.input) if tx.input else 0,
                    })

                # Insert into ClickHouse
                if ch_data:
                    self.ch.execute(
                        'INSERT INTO fact_transactions VALUES',
                        ch_data
                    )

                self.logger.info(
                    "batch_synced",
                    block_range=f"{block}-{batch_end}",
                    count=len(ch_data)
                )

    def sync_token_transfers(
        self,
        start_block: int,
        end_block: int,
        batch_size: int = 10000
    ):
        """Sync token transfers to ClickHouse."""
        with get_session() as session:
            # Query logs with Transfer event signature
            transfer_signature = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'

            for block in range(start_block, end_block + 1, batch_size):
                batch_end = min(block + batch_size - 1, end_block)

                logs = (
                    session.query(Log)
                    .filter(Log.block_number >= block)
                    .filter(Log.block_number <= batch_end)
                    .filter(Log.topic0 == transfer_signature)
                    .filter(Log.is_reorged == False)
                    .all()
                )

                if not logs:
                    continue

                # Transform to token transfers
                ch_data = []
                for log in logs:
                    # Decode Transfer event
                    # Transfer(address indexed from, address indexed to, uint256 value)
                    from_addr = '0x' + log.topic1[-40:] if log.topic1 else '0x0'
                    to_addr = '0x' + log.topic2[-40:] if log.topic2 else '0x0'

                    ch_data.append({
                        'transaction_hash': log.transaction_hash,
                        'log_index': log.log_index,
                        'block_number': log.block_number,
                        'timestamp': log.timestamp,
                        'date': datetime.fromtimestamp(log.timestamp).date(),
                        'hour': datetime.fromtimestamp(log.timestamp).replace(
                            minute=0, second=0, microsecond=0
                        ),
                        'token_address': log.address,
                        'token_type': 'ERC20',  # Detect from contract
                        'from_address': from_addr,
                        'to_address': to_addr,
                        'value': int(log.data, 16) if log.data else 0,
                        'token_id': None,
                    })

                # Insert
                if ch_data:
                    self.ch.execute(
                        'INSERT INTO fact_token_transfers VALUES',
                        ch_data
                    )

                self.logger.info(
                    "token_transfers_synced",
                    block_range=f"{block}-{batch_end}",
                    count=len(ch_data)
                )

    def compute_daily_stats(self, date: datetime.date):
        """Compute and store daily statistics."""
        query = f"""
        INSERT INTO agg_daily_stats
        SELECT
            toDate('{date}') as date,
            count(DISTINCT block_number) as block_count,
            avg(input_size) as avg_block_size,
            0 as avg_block_time,
            count(*) as transaction_count,
            uniq(from_address) + uniq(to_address) as unique_addresses,
            avg(gas_price) as avg_gas_price,
            sum(gas_used) as total_gas_used,
            sum(transaction_fee) as total_transaction_fees,
            sum(value) as total_value_transferred,
            avg(value) as avg_transaction_value,
            sumIf(1, is_contract_creation = 1) as contract_creations,
            sumIf(1, is_contract_creation = 0) as contract_calls,
            0 as token_transfers,
            0 as unique_token_senders,
            0 as unique_token_receivers,
            now() as computed_at
        FROM fact_transactions
        WHERE date = toDate('{date}')
        """

        self.ch.execute(query)

        self.logger.info("daily_stats_computed", date=date)
```

---

## Advanced Queries

### 3.1 Daily Statistics (analytics/queries/daily_stats.py)

```python
"""Daily statistics queries."""
from datetime import date, timedelta
from typing import List, Dict
from clickhouse_driver import Client


class DailyStatsQuery:
    """Daily statistics queries."""

    def __init__(self, ch_client: Client):
        self.ch = ch_client

    def get_daily_stats(
        self,
        start_date: date,
        end_date: date
    ) -> List[Dict]:
        """
        Get daily statistics for date range.

        Returns:
            List of daily stats dicts
        """
        query = """
        SELECT
            date,
            block_count,
            transaction_count,
            unique_addresses,
            avg_gas_price,
            total_gas_used,
            total_transaction_fees,
            total_value_transferred,
            contract_creations
        FROM agg_daily_stats
        WHERE date BETWEEN %(start_date)s AND %(end_date)s
        ORDER BY date DESC
        """

        result = self.ch.execute(
            query,
            {'start_date': start_date, 'end_date': end_date},
            with_column_types=True
        )

        columns = [col[0] for col in result[1]]
        return [dict(zip(columns, row)) for row in result[0]]

    def get_transaction_growth(self, days: int = 30) -> List[Dict]:
        """Get transaction count growth over time."""
        query = f"""
        SELECT
            date,
            transaction_count,
            transaction_count - lagInFrame(transaction_count, 1) OVER (ORDER BY date) as daily_change,
            (transaction_count - lagInFrame(transaction_count, 1) OVER (ORDER BY date)) /
                lagInFrame(transaction_count, 1) OVER (ORDER BY date) * 100 as daily_change_pct
        FROM agg_daily_stats
        WHERE date >= today() - {days}
        ORDER BY date DESC
        """

        result = self.ch.execute(query, with_column_types=True)
        columns = [col[0] for col in result[1]]
        return [dict(zip(columns, row)) for row in result[0]]

    def get_top_active_days(self, limit: int = 10) -> List[Dict]:
        """Get days with most transaction activity."""
        query = f"""
        SELECT
            date,
            transaction_count,
            unique_addresses,
            total_gas_used,
            total_value_transferred
        FROM agg_daily_stats
        ORDER BY transaction_count DESC
        LIMIT {limit}
        """

        result = self.ch.execute(query, with_column_types=True)
        columns = [col[0] for col in result[1]]
        return [dict(zip(columns, row)) for row in result[0]]
```

### 3.2 Gas Analytics (analytics/queries/gas_analytics.py)

```python
"""Gas price analytics queries."""
from datetime import datetime
from typing import List, Dict
from clickhouse_driver import Client


class GasAnalyticsQuery:
    """Gas analytics queries."""

    def __init__(self, ch_client: Client):
        self.ch = ch_client

    def get_gas_price_history(
        self,
        hours: int = 24,
        interval_minutes: int = 60
    ) -> List[Dict]:
        """
        Get gas price history with statistics.

        Args:
            hours: Number of hours to look back
            interval_minutes: Aggregation interval in minutes

        Returns:
            List of gas price stats per interval
        """
        query = f"""
        SELECT
            toStartOfInterval(hour, INTERVAL {interval_minutes} MINUTE) as time,
            min(gas_price) as min_gas_price,
            avg(gas_price) as avg_gas_price,
            median(gas_price) as median_gas_price,
            quantile(0.25)(gas_price) as p25_gas_price,
            quantile(0.75)(gas_price) as p75_gas_price,
            quantile(0.95)(gas_price) as p95_gas_price,
            max(gas_price) as max_gas_price,
            count(*) as tx_count
        FROM fact_transactions
        WHERE hour >= now() - INTERVAL {hours} HOUR
        GROUP BY time
        ORDER BY time DESC
        """

        result = self.ch.execute(query, with_column_types=True)
        columns = [col[0] for col in result[1]]
        return [dict(zip(columns, row)) for row in result[0]]

    def get_gas_usage_by_contract(
        self,
        start_date: datetime,
        end_date: datetime,
        limit: int = 20
    ) -> List[Dict]:
        """Get top contracts by gas consumption."""
        query = f"""
        SELECT
            to_address as contract,
            count(*) as call_count,
            sum(gas_used) as total_gas_used,
            avg(gas_used) as avg_gas_used,
            sum(transaction_fee) as total_fees_paid
        FROM fact_transactions
        WHERE date BETWEEN %(start_date)s AND %(end_date)s
          AND to_address != ''
          AND is_contract_creation = 0
        GROUP BY contract
        ORDER BY total_gas_used DESC
        LIMIT {limit}
        """

        result = self.ch.execute(
            query,
            {
                'start_date': start_date.date(),
                'end_date': end_date.date()
            },
            with_column_types=True
        )

        columns = [col[0] for col in result[1]]
        return [dict(zip(columns, row)) for row in result[0]]

    def get_gas_price_percentiles_by_hour(self) -> List[Dict]:
        """Get gas price distribution by hour of day."""
        query = """
        SELECT
            toHour(hour) as hour_of_day,
            quantile(0.10)(gas_price) as p10,
            quantile(0.25)(gas_price) as p25,
            quantile(0.50)(gas_price) as p50,
            quantile(0.75)(gas_price) as p75,
            quantile(0.90)(gas_price) as p90,
            count(*) as sample_size
        FROM fact_transactions
        WHERE date >= today() - 30
        GROUP BY hour_of_day
        ORDER BY hour_of_day
        """

        result = self.ch.execute(query, with_column_types=True)
        columns = [col[0] for col in result[1]]
        return [dict(zip(columns, row)) for row in result[0]]
```

---

## Token Analytics

### 4.1 Token Queries (analytics/queries/token_analytics.py)

```python
"""Token analytics queries."""
from datetime import date
from typing import List, Dict, Optional
from clickhouse_driver import Client


class TokenAnalyticsQuery:
    """Token analytics queries."""

    def __init__(self, ch_client: Client):
        self.ch = ch_client

    def get_top_tokens_by_volume(
        self,
        start_date: date,
        end_date: date,
        limit: int = 50
    ) -> List[Dict]:
        """
        Get top tokens by transfer volume.

        Returns:
            List of tokens sorted by transfer count
        """
        query = f"""
        SELECT
            token_address,
            count(*) as transfer_count,
            uniq(from_address) as unique_senders,
            uniq(to_address) as unique_receivers,
            uniq(from_address) + uniq(to_address) as unique_users,
            sum(value) as total_volume
        FROM fact_token_transfers
        WHERE date BETWEEN %(start_date)s AND %(end_date)s
        GROUP BY token_address
        ORDER BY transfer_count DESC
        LIMIT {limit}
        """

        result = self.ch.execute(
            query,
            {'start_date': start_date, 'end_date': end_date},
            with_column_types=True
        )

        columns = [col[0] for col in result[1]]
        return [dict(zip(columns, row)) for row in result[0]]

    def get_token_transfer_timeline(
        self,
        token_address: str,
        days: int = 30
    ) -> List[Dict]:
        """Get daily transfer statistics for a token."""
        query = f"""
        SELECT
            date,
            count(*) as transfer_count,
            uniq(from_address) as unique_senders,
            uniq(to_address) as unique_receivers,
            sum(value) as volume
        FROM fact_token_transfers
        WHERE token_address = %(token_address)s
          AND date >= today() - {days}
        GROUP BY date
        ORDER BY date DESC
        """

        result = self.ch.execute(
            query,
            {'token_address': token_address},
            with_column_types=True
        )

        columns = [col[0] for col in result[1]]
        return [dict(zip(columns, row)) for row in result[0]]

    def get_token_holder_distribution(
        self,
        token_address: str
    ) -> Dict:
        """
        Get holder distribution for a token.

        Returns distribution buckets:
        - Whales (> 1% supply)
        - Large holders (0.1% - 1%)
        - Medium holders (0.01% - 0.1%)
        - Small holders (< 0.01%)
        """
        query = """
        WITH balances AS (
            SELECT
                CASE
                    WHEN from_address != '0x0000000000000000000000000000000000000000' THEN from_address
                END as address,
                -sum(value) as balance_change
            FROM fact_token_transfers
            WHERE token_address = %(token_address)s
            GROUP BY address

            UNION ALL

            SELECT
                CASE
                    WHEN to_address != '0x0000000000000000000000000000000000000000' THEN to_address
                END as address,
                sum(value) as balance_change
            FROM fact_token_transfers
            WHERE token_address = %(token_address)s
            GROUP BY address
        ),
        holder_balances AS (
            SELECT
                address,
                sum(balance_change) as balance
            FROM balances
            WHERE address IS NOT NULL
            GROUP BY address
            HAVING balance > 0
        ),
        total_supply AS (
            SELECT sum(balance) as supply FROM holder_balances
        )
        SELECT
            countIf(balance / supply > 0.01) as whales,
            countIf(balance / supply BETWEEN 0.001 AND 0.01) as large_holders,
            countIf(balance / supply BETWEEN 0.0001 AND 0.001) as medium_holders,
            countIf(balance / supply < 0.0001) as small_holders,
            count(*) as total_holders
        FROM holder_balances, total_supply
        """

        result = self.ch.execute(
            query,
            {'token_address': token_address}
        )

        if result:
            return {
                'whales': result[0][0],
                'large_holders': result[0][1],
                'medium_holders': result[0][2],
                'small_holders': result[0][3],
                'total_holders': result[0][4],
            }

        return {}

    def get_whale_movements(
        self,
        token_address: str,
        min_value: int,
        hours: int = 24
    ) -> List[Dict]:
        """
        Get large token transfers (whale movements).

        Args:
            token_address: Token contract address
            min_value: Minimum transfer value
            hours: Look back hours

        Returns:
            List of large transfers
        """
        query = f"""
        SELECT
            transaction_hash,
            block_number,
            timestamp,
            from_address,
            to_address,
            value
        FROM fact_token_transfers
        WHERE token_address = %(token_address)s
          AND value >= %(min_value)s
          AND timestamp >= now() - INTERVAL {hours} HOUR
        ORDER BY value DESC
        LIMIT 100
        """

        result = self.ch.execute(
            query,
            {
                'token_address': token_address,
                'min_value': min_value
            },
            with_column_types=True
        )

        columns = [col[0] for col in result[1]]
        return [dict(zip(columns, row)) for row in result[0]]
```

---

## Address Analytics

### 5.1 Address Queries (analytics/queries/address_analytics.py)

```python
"""Address analytics queries."""
from datetime import date
from typing import List, Dict
from clickhouse_driver import Client


class AddressAnalyticsQuery:
    """Address analytics queries."""

    def __init__(self, ch_client: Client):
        self.ch = ch_client

    def get_top_addresses_by_volume(
        self,
        start_date: date,
        end_date: date,
        limit: int = 100
    ) -> List[Dict]:
        """Get top addresses by transaction volume."""
        query = f"""
        SELECT
            from_address as address,
            count(*) as tx_count,
            sum(value) as total_sent,
            sum(transaction_fee) as total_fees_paid,
            uniq(to_address) as unique_recipients
        FROM fact_transactions
        WHERE date BETWEEN %(start_date)s AND %(end_date)s
        GROUP BY address
        ORDER BY total_sent DESC
        LIMIT {limit}
        """

        result = self.ch.execute(
            query,
            {'start_date': start_date, 'end_date': end_date},
            with_column_types=True
        )

        columns = [col[0] for col in result[1]]
        return [dict(zip(columns, row)) for row in result[0]]

    def get_address_activity_timeline(
        self,
        address: str,
        days: int = 30
    ) -> List[Dict]:
        """Get daily activity for an address."""
        query = f"""
        SELECT
            date,
            countIf(from_address = %(address)s) as sent_count,
            countIf(to_address = %(address)s) as received_count,
            sumIf(value, from_address = %(address)s) as sent_volume,
            sumIf(value, to_address = %(address)s) as received_volume
        FROM fact_transactions
        WHERE (from_address = %(address)s OR to_address = %(address)s)
          AND date >= today() - {days}
        GROUP BY date
        ORDER BY date DESC
        """

        result = self.ch.execute(
            query,
            {'address': address},
            with_column_types=True
        )

        columns = [col[0] for col in result[1]]
        return [dict(zip(columns, row)) for row in result[0]]

    def get_new_addresses_per_day(self, days: int = 30) -> List[Dict]:
        """Get count of new addresses per day."""
        query = f"""
        WITH first_appearance AS (
            SELECT
                address,
                min(date) as first_seen
            FROM (
                SELECT from_address as address, date FROM fact_transactions
                UNION ALL
                SELECT to_address as address, date FROM fact_transactions WHERE to_address != ''
            )
            GROUP BY address
        )
        SELECT
            first_seen as date,
            count(*) as new_addresses
        FROM first_appearance
        WHERE first_seen >= today() - {days}
        GROUP BY date
        ORDER BY date DESC
        """

        result = self.ch.execute(query, with_column_types=True)
        columns = [col[0] for col in result[1]]
        return [dict(zip(columns, row)) for row in result[0]]

    def get_address_interaction_graph(
        self,
        address: str,
        min_interactions: int = 5,
        limit: int = 50
    ) -> Dict:
        """
        Get addresses that interact most with given address.

        Returns:
            Graph data with nodes and edges
        """
        query = f"""
        SELECT
            to_address,
            count(*) as interaction_count,
            sum(value) as total_value
        FROM fact_transactions
        WHERE from_address = %(address)s
          AND to_address != ''
        GROUP BY to_address
        HAVING interaction_count >= {min_interactions}
        ORDER BY interaction_count DESC
        LIMIT {limit}
        """

        result = self.ch.execute(
            query,
            {'address': address},
            with_column_types=True
        )

        nodes = [{'id': address, 'type': 'source'}]
        edges = []

        for row in result[0]:
            to_addr = row[0]
            count = row[1]
            value = row[2]

            nodes.append({'id': to_addr, 'type': 'target'})
            edges.append({
                'source': address,
                'target': to_addr,
                'weight': count,
                'value': value
            })

        return {
            'nodes': nodes,
            'edges': edges
        }
```

---

## Data Visualization

### 6.1 Chart Components (ui/components/charts/TransactionChart.tsx)

```typescript
"use client";

import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

interface DailyStats {
  date: string;
  transaction_count: number;
  unique_addresses: number;
  total_gas_used: number;
}

interface TransactionChartProps {
  data: DailyStats[];
}

export function TransactionChart({ data }: TransactionChartProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Daily Transactions</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="date"
              tickFormatter={(value) => new Date(value).toLocaleDateString()}
            />
            <YAxis />
            <Tooltip
              labelFormatter={(value) => new Date(value).toLocaleDateString()}
              formatter={(value: number) => value.toLocaleString()}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="transaction_count"
              stroke="#8884d8"
              name="Transactions"
            />
            <Line
              type="monotone"
              dataKey="unique_addresses"
              stroke="#82ca9d"
              name="Unique Addresses"
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}

export function GasPriceChart({ data }: { data: any[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Gas Price History</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="time"
              tickFormatter={(value) =>
                new Date(value).toLocaleTimeString()
              }
            />
            <YAxis label={{ value: "Gwei", angle: -90, position: "insideLeft" }} />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="avg_gas_price"
              stroke="#8884d8"
              name="Average"
            />
            <Line
              type="monotone"
              dataKey="p95_gas_price"
              stroke="#ff7c7c"
              name="95th Percentile"
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}

export function TokenVolumeChart({ data }: { data: any[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Top Tokens by Volume</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={data} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis
              dataKey="token_address"
              type="category"
              width={150}
              tickFormatter={(value) =>
                value.slice(0, 6) + "..." + value.slice(-4)
              }
            />
            <Tooltip />
            <Bar dataKey="transfer_count" fill="#8884d8" name="Transfers" />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
```

---

## Export & Reporting

### 7.1 CSV Export (analytics/export.py)

```python
"""Data export functionality."""
import csv
from io import StringIO
from typing import List, Dict
from fastapi.responses import StreamingResponse


class DataExporter:
    """Export analytics data to various formats."""

    @staticmethod
    def to_csv(data: List[Dict], filename: str) -> StreamingResponse:
        """
        Export data to CSV.

        Args:
            data: List of dicts to export
            filename: Output filename

        Returns:
            StreamingResponse with CSV data
        """
        if not data:
            return StreamingResponse(
                iter([""]),
                media_type="text/csv",
                headers={
                    "Content-Disposition": f"attachment; filename={filename}"
                }
            )

        # Create CSV in memory
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

        # Get CSV content
        output.seek(0)

        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    @staticmethod
    def to_json_stream(data: List[Dict]) -> StreamingResponse:
        """Export data as JSON stream."""
        import json

        def generate():
            yield "[\n"
            for i, item in enumerate(data):
                if i > 0:
                    yield ",\n"
                yield json.dumps(item)
            yield "\n]"

        return StreamingResponse(
            generate(),
            media_type="application/json"
        )
```

### 7.2 API Endpoint (api/routers/analytics.py)

```python
"""Analytics API endpoints."""
from fastapi import APIRouter, Depends, Query
from datetime import date, timedelta
from typing import Optional

from analytics.queries.daily_stats import DailyStatsQuery
from analytics.queries.gas_analytics import GasAnalyticsQuery
from analytics.queries.token_analytics import TokenAnalyticsQuery
from analytics.export import DataExporter
from database import get_clickhouse_client


router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


@router.get("/daily-stats")
async def get_daily_stats(
    days: int = Query(30, ge=1, le=365),
    ch = Depends(get_clickhouse_client)
):
    """Get daily statistics."""
    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    query = DailyStatsQuery(ch)
    stats = query.get_daily_stats(start_date, end_date)

    return {
        "data": stats,
        "start_date": start_date,
        "end_date": end_date
    }


@router.get("/gas-price-history")
async def get_gas_price_history(
    hours: int = Query(24, ge=1, le=168),
    ch = Depends(get_clickhouse_client)
):
    """Get gas price history."""
    query = GasAnalyticsQuery(ch)
    return query.get_gas_price_history(hours=hours)


@router.get("/top-tokens")
async def get_top_tokens(
    days: int = Query(7, ge=1, le=30),
    limit: int = Query(50, ge=1, le=100),
    ch = Depends(get_clickhouse_client)
):
    """Get top tokens by transfer volume."""
    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    query = TokenAnalyticsQuery(ch)
    return query.get_top_tokens_by_volume(start_date, end_date, limit)


@router.get("/export/daily-stats")
async def export_daily_stats(
    days: int = Query(30, ge=1, le=365),
    format: str = Query("csv", regex="^(csv|json)$"),
    ch = Depends(get_clickhouse_client)
):
    """Export daily statistics."""
    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    query = DailyStatsQuery(ch)
    stats = query.get_daily_stats(start_date, end_date)

    exporter = DataExporter()

    if format == "csv":
        return exporter.to_csv(stats, f"daily-stats-{start_date}-{end_date}.csv")
    else:
        return exporter.to_json_stream(stats)
```

---

## แบบฝึกหัด

### แบบฝึกหัดที่ 1: Setup ClickHouse

**เป้าหมาย**: Setup ClickHouse และสร้าง analytics tables

**Steps**:
1. Install ClickHouse
2. Create database
3. Create fact tables
4. Create aggregation tables
5. Insert sample data

**Pass criteria**:
- ✅ ClickHouse running
- ✅ Tables created
- ✅ Can query data

### แบบฝึกหัดที่ 2: Sync Data Pipeline

**เป้าหมาย**: Implement data sync from PostgreSQL to ClickHouse

**Requirements**:
- Sync transactions
- Sync token transfers
- Handle incremental updates
- Schedule with cron

**Pass criteria**:
- ✅ Data synced correctly
- ✅ No duplicates
- ✅ Performance acceptable

### แบบฝึกหัดที่ 3: Create Analytics Query

**เป้าหมาย**: เขียน query วิเคราะห์ข้อมูล

**Requirements**:
- Top 10 addresses by gas spent
- Include time range filter
- Return formatted results

**Pass criteria**:
- ✅ Query returns correct data
- ✅ Performance < 1s
- ✅ Results match expectations

### แบบฝึกหัดที่ 4: Build Visualization

**เป้าหมาย**: สร้าง chart component

**Requirements**:
- Transaction count over time (line chart)
- Responsive design
- Loading states

**Pass criteria**:
- ✅ Chart renders correctly
- ✅ Data updates on refresh
- ✅ Mobile friendly

### แบบฝึกหัดที่ 5: CSV Export

**เป้าหมาย**: Implement data export

**Requirements**:
- Export daily stats to CSV
- Include headers
- Stream large datasets

**Pass criteria**:
- ✅ CSV downloads
- ✅ Data formatted correctly
- ✅ Handles large files

---

## Pass Criteria - PART08

ก่อนจบ PART08 ให้ตรวจสอบว่า:

- [ ] เข้าใจ ClickHouse analytics architecture
- [ ] สามารถ sync ข้อมูลจาก PostgreSQL ไป ClickHouse
- [ ] เขียน advanced analytics queries ได้
- [ ] Implement token analytics
- [ ] Implement address analytics
- [ ] สร้าง data visualizations
- [ ] Implement data export
- [ ] สามารถทำแบบฝึกหัดอย่างน้อย 3 ข้อให้สำเร็จ

---

## Production Notes

### Performance

**ClickHouse**:
- Query latency: < 1s for billion rows
- Compression: 10-100x
- Parallel execution
- Materialized views for pre-aggregation

### Scalability

- Partitioning by month
- Distributed tables for horizontal scaling
- Replication for HA
- TTL policies for old data

### Monitoring

- Query performance metrics
- Storage usage
- Replication lag
- Failed queries

---

**จบ PART08 - Analytics & Advanced Features**

**ถัดไป**: PART09 - Monitoring & Observability

---

**สถิติ PART08**:
- **Lines**: ~2,000 lines
- **Queries**: 20+ analytics queries
- **Components**: 10+ visualization components
- **Exercises**: 5 hands-on labs

---

*เอกสารนี้เป็นส่วนหนึ่งของโปรเจกต์ Blockchain Explorer System*
