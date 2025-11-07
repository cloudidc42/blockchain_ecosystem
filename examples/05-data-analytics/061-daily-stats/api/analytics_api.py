"""
Analytics API
FastAPI endpoints for querying blockchain analytics from ClickHouse
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date, timedelta
from clickhouse_driver import Client
import os

# Pydantic models
class DailyBlockStats(BaseModel):
    """Daily block statistics"""
    date: date
    block_count: int
    avg_block_time: float
    min_block_number: int
    max_block_number: int
    total_transactions: int
    avg_transactions_per_block: float
    total_gas_used: int
    avg_gas_used: float
    total_gas_limit: int
    avg_gas_limit: float
    gas_usage_percentage: float
    unique_miners: int

class DailyTransactionStats(BaseModel):
    """Daily transaction statistics"""
    date: date
    transaction_count: int
    avg_gas_price: float
    median_gas_price: float
    min_gas_price: int
    max_gas_price: int
    avg_transaction_value: float
    total_transaction_value: float
    failed_transactions: int
    success_rate: float
    avg_gas_used: float
    contract_creations: int
    contract_calls: int

class HourlyBlockStats(BaseModel):
    """Hourly block statistics"""
    datetime: datetime
    hour: int
    date: date
    block_count: int
    avg_block_time: float
    total_transactions: int
    total_gas_used: int
    avg_gas_used: float
    unique_miners: int

class MinerStats(BaseModel):
    """Miner statistics"""
    date: date
    miner: str
    blocks_mined: int
    total_gas_collected: int
    total_transactions: int

class TimeSeriesPoint(BaseModel):
    """Generic time series data point"""
    timestamp: datetime
    value: float
    label: Optional[str] = None

class AnalyticsSummary(BaseModel):
    """Analytics summary response"""
    period: str
    total_blocks: int
    total_transactions: int
    avg_block_time: float
    avg_gas_price: float
    total_value_transferred: float
    unique_miners: int
    avg_gas_usage_pct: float

# Create FastAPI app
app = FastAPI(
    title="Blockchain Analytics API",
    version="1.0.0",
    description="Analytics API for blockchain data powered by ClickHouse"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ClickHouse connection
def get_clickhouse_client():
    """Get ClickHouse client"""
    return Client(
        host=os.getenv('CLICKHOUSE_HOST', 'localhost'),
        port=int(os.getenv('CLICKHOUSE_PORT', '9000')),
        user=os.getenv('CLICKHOUSE_USER', 'default'),
        password=os.getenv('CLICKHOUSE_PASSWORD', ''),
        database=os.getenv('CLICKHOUSE_DATABASE', 'blockchain_analytics')
    )

# Endpoints

@app.get("/")
async def root():
    """API root"""
    return {
        "name": "Blockchain Analytics API",
        "version": "1.0.0",
        "endpoints": {
            "daily_blocks": "/api/analytics/daily/blocks",
            "daily_transactions": "/api/analytics/daily/transactions",
            "hourly_blocks": "/api/analytics/hourly/blocks",
            "miners": "/api/analytics/miners",
            "summary": "/api/analytics/summary",
            "trends": "/api/analytics/trends"
        }
    }

@app.get("/health")
async def health_check():
    """Health check"""
    try:
        client = get_clickhouse_client()
        result = client.execute("SELECT 1")
        return {
            "status": "healthy",
            "clickhouse": "connected",
            "version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"ClickHouse error: {str(e)}")

@app.get("/api/analytics/daily/blocks", response_model=List[DailyBlockStats])
async def get_daily_blocks(
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(30, ge=1, le=365, description="Number of days to return")
):
    """
    Get daily block statistics

    Returns aggregated block statistics by day
    """
    try:
        client = get_clickhouse_client()

        # Default date range
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=limit)

        query = """
        SELECT
            date,
            block_count,
            avg_block_time,
            min_block_number,
            max_block_number,
            total_transactions,
            avg_transactions_per_block,
            total_gas_used,
            avg_gas_used,
            total_gas_limit,
            avg_gas_limit,
            gas_usage_percentage,
            unique_miners
        FROM daily_blocks
        WHERE date >= %(start_date)s AND date <= %(end_date)s
        ORDER BY date DESC
        LIMIT %(limit)s
        """

        result = client.execute(
            query,
            {
                'start_date': start_date,
                'end_date': end_date,
                'limit': limit
            }
        )

        return [
            DailyBlockStats(
                date=row[0],
                block_count=row[1],
                avg_block_time=row[2],
                min_block_number=row[3],
                max_block_number=row[4],
                total_transactions=row[5],
                avg_transactions_per_block=row[6],
                total_gas_used=row[7],
                avg_gas_used=row[8],
                total_gas_limit=row[9],
                avg_gas_limit=row[10],
                gas_usage_percentage=row[11],
                unique_miners=row[12]
            )
            for row in result
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/daily/transactions", response_model=List[DailyTransactionStats])
async def get_daily_transactions(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    limit: int = Query(30, ge=1, le=365)
):
    """
    Get daily transaction statistics

    Returns aggregated transaction statistics by day
    """
    try:
        client = get_clickhouse_client()

        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=limit)

        query = """
        SELECT
            date,
            transaction_count,
            avg_gas_price,
            median_gas_price,
            min_gas_price,
            max_gas_price,
            avg_transaction_value,
            total_transaction_value,
            failed_transactions,
            success_rate,
            avg_gas_used,
            contract_creations,
            contract_calls
        FROM daily_transactions
        WHERE date >= %(start_date)s AND date <= %(end_date)s
        ORDER BY date DESC
        LIMIT %(limit)s
        """

        result = client.execute(
            query,
            {
                'start_date': start_date,
                'end_date': end_date,
                'limit': limit
            }
        )

        return [
            DailyTransactionStats(
                date=row[0],
                transaction_count=row[1],
                avg_gas_price=row[2],
                median_gas_price=row[3],
                min_gas_price=row[4],
                max_gas_price=row[5],
                avg_transaction_value=row[6],
                total_transaction_value=row[7],
                failed_transactions=row[8],
                success_rate=row[9],
                avg_gas_used=row[10],
                contract_creations=row[11],
                contract_calls=row[12]
            )
            for row in result
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/hourly/blocks", response_model=List[HourlyBlockStats])
async def get_hourly_blocks(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    hours: int = Query(24, ge=1, le=168, description="Number of hours to return")
):
    """
    Get hourly block statistics

    Returns aggregated block statistics by hour
    """
    try:
        client = get_clickhouse_client()

        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=7)

        query = """
        SELECT
            datetime,
            hour,
            date,
            block_count,
            avg_block_time,
            total_transactions,
            total_gas_used,
            avg_gas_used,
            unique_miners
        FROM hourly_blocks
        WHERE date >= %(start_date)s AND date <= %(end_date)s
        ORDER BY datetime DESC
        LIMIT %(hours)s
        """

        result = client.execute(
            query,
            {
                'start_date': start_date,
                'end_date': end_date,
                'hours': hours
            }
        )

        return [
            HourlyBlockStats(
                datetime=row[0],
                hour=row[1],
                date=row[2],
                block_count=row[3],
                avg_block_time=row[4],
                total_transactions=row[5],
                total_gas_used=row[6],
                avg_gas_used=row[7],
                unique_miners=row[8]
            )
            for row in result
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/miners", response_model=List[MinerStats])
async def get_top_miners(
    target_date: Optional[date] = Query(None, description="Date to query"),
    limit: int = Query(10, ge=1, le=100, description="Number of miners to return")
):
    """
    Get top miners for a specific date

    Returns top miners by blocks mined
    """
    try:
        client = get_clickhouse_client()

        if not target_date:
            target_date = date.today()

        query = """
        SELECT
            date,
            miner,
            blocks_mined,
            total_gas_collected,
            total_transactions
        FROM daily_miners
        WHERE date = %(target_date)s
        ORDER BY blocks_mined DESC
        LIMIT %(limit)s
        """

        result = client.execute(
            query,
            {
                'target_date': target_date,
                'limit': limit
            }
        )

        return [
            MinerStats(
                date=row[0],
                miner=row[1],
                blocks_mined=row[2],
                total_gas_collected=row[3],
                total_transactions=row[4]
            )
            for row in result
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(
    period: str = Query("7d", description="Period: 1d, 7d, 30d, 90d"),
):
    """
    Get analytics summary for a period

    Returns aggregated metrics for the specified period
    """
    try:
        client = get_clickhouse_client()

        # Parse period
        days_map = {
            '1d': 1,
            '7d': 7,
            '30d': 30,
            '90d': 90
        }

        days = days_map.get(period, 7)
        start_date = date.today() - timedelta(days=days)

        # Query blocks
        blocks_query = """
        SELECT
            SUM(block_count) as total_blocks,
            SUM(total_transactions) as total_transactions,
            AVG(avg_block_time) as avg_block_time,
            AVG(gas_usage_percentage) as avg_gas_usage_pct,
            COUNT(DISTINCT unique_miners) as unique_miners
        FROM daily_blocks
        WHERE date >= %(start_date)s
        """

        blocks_result = client.execute(blocks_query, {'start_date': start_date})

        # Query transactions
        tx_query = """
        SELECT
            AVG(avg_gas_price) as avg_gas_price,
            SUM(total_transaction_value) as total_value
        FROM daily_transactions
        WHERE date >= %(start_date)s
        """

        tx_result = client.execute(tx_query, {'start_date': start_date})

        if blocks_result and tx_result:
            return AnalyticsSummary(
                period=period,
                total_blocks=blocks_result[0][0] or 0,
                total_transactions=blocks_result[0][1] or 0,
                avg_block_time=blocks_result[0][2] or 0,
                avg_gas_usage_pct=blocks_result[0][3] or 0,
                unique_miners=blocks_result[0][4] or 0,
                avg_gas_price=tx_result[0][0] or 0,
                total_value_transferred=tx_result[0][1] or 0
            )
        else:
            raise HTTPException(status_code=404, detail="No data found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/trends/blocks", response_model=List[TimeSeriesPoint])
async def get_block_trends(
    days: int = Query(30, ge=1, le=365, description="Number of days")
):
    """
    Get block count trends

    Returns daily block counts as a time series
    """
    try:
        client = get_clickhouse_client()

        start_date = date.today() - timedelta(days=days)

        query = """
        SELECT
            date,
            block_count
        FROM daily_blocks
        WHERE date >= %(start_date)s
        ORDER BY date ASC
        """

        result = client.execute(query, {'start_date': start_date})

        return [
            TimeSeriesPoint(
                timestamp=datetime.combine(row[0], datetime.min.time()),
                value=float(row[1]),
                label="blocks"
            )
            for row in result
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/trends/gas", response_model=List[TimeSeriesPoint])
async def get_gas_price_trends(
    days: int = Query(30, ge=1, le=365)
):
    """
    Get gas price trends

    Returns daily average gas prices as a time series
    """
    try:
        client = get_clickhouse_client()

        start_date = date.today() - timedelta(days=days)

        query = """
        SELECT
            date,
            avg_gas_price
        FROM daily_transactions
        WHERE date >= %(start_date)s
        ORDER BY date ASC
        """

        result = client.execute(query, {'start_date': start_date})

        return [
            TimeSeriesPoint(
                timestamp=datetime.combine(row[0], datetime.min.time()),
                value=float(row[1]),
                label="gas_price_gwei"
            )
            for row in result
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
