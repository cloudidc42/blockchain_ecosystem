"""
Blockchain ETL Script
Extracts blockchain data, transforms it, and loads into ClickHouse for analytics
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import statistics

from web3 import Web3
from web3.exceptions import BlockNotFound
from clickhouse_driver import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BlockchainETL:
    """ETL pipeline for blockchain analytics"""

    def __init__(
        self,
        rpc_url: Optional[str] = None,
        clickhouse_host: str = "localhost",
        clickhouse_port: int = 9000,
        clickhouse_user: str = "default",
        clickhouse_password: str = "",
        clickhouse_database: str = "blockchain_analytics"
    ):
        """
        Initialize ETL pipeline

        Args:
            rpc_url: Blockchain RPC endpoint
            clickhouse_host: ClickHouse server host
            clickhouse_port: ClickHouse native protocol port
            clickhouse_user: ClickHouse username
            clickhouse_password: ClickHouse password
            clickhouse_database: ClickHouse database name
        """
        # Web3 connection
        self.rpc_url = rpc_url or os.getenv('RPC_URL', 'http://localhost:8545')
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))

        # ClickHouse connection
        self.ch_client = Client(
            host=clickhouse_host,
            port=clickhouse_port,
            user=clickhouse_user,
            password=clickhouse_password,
            database=clickhouse_database
        )

        print(f"✅ Connected to blockchain: {self.w3.is_connected()}")
        print(f"✅ ClickHouse connection established")

    def get_blocks_in_range(
        self,
        start_block: int,
        end_block: int,
        include_transactions: bool = True
    ) -> List[Dict]:
        """
        Fetch blocks in a range

        Args:
            start_block: Starting block number
            end_block: Ending block number (inclusive)
            include_transactions: Whether to include full transaction data

        Returns:
            List of block dictionaries
        """
        blocks = []

        for block_num in range(start_block, end_block + 1):
            try:
                block = self.w3.eth.get_block(block_num, full_transactions=include_transactions)
                blocks.append(dict(block))

                if (block_num - start_block + 1) % 100 == 0:
                    print(f"  Fetched {block_num - start_block + 1}/{end_block - start_block + 1} blocks")

            except BlockNotFound:
                print(f"⚠️  Block {block_num} not found, stopping")
                break
            except Exception as e:
                print(f"❌ Error fetching block {block_num}: {e}")
                continue

        return blocks

    def get_blocks_by_date(
        self,
        target_date: datetime,
        include_transactions: bool = True
    ) -> List[Dict]:
        """
        Fetch all blocks for a specific date

        Args:
            target_date: Date to fetch blocks for
            include_transactions: Whether to include full transaction data

        Returns:
            List of block dictionaries
        """
        # Get timestamp range for the date
        start_timestamp = int(target_date.replace(hour=0, minute=0, second=0).timestamp())
        end_timestamp = int((target_date + timedelta(days=1)).replace(hour=0, minute=0, second=0).timestamp())

        # Find approximate block range using binary search
        latest_block = self.w3.eth.block_number

        # Find start block
        start_block = self._find_block_by_timestamp(start_timestamp, 0, latest_block)

        # Find end block
        end_block = self._find_block_by_timestamp(end_timestamp, start_block, latest_block)

        print(f"📅 Date: {target_date.date()}")
        print(f"🔢 Block range: {start_block} - {end_block} ({end_block - start_block + 1} blocks)")

        return self.get_blocks_in_range(start_block, end_block, include_transactions)

    def _find_block_by_timestamp(
        self,
        target_timestamp: int,
        low: int,
        high: int,
        tolerance: int = 60
    ) -> int:
        """
        Binary search to find block by timestamp

        Args:
            target_timestamp: Target Unix timestamp
            low: Lower bound block number
            high: Upper bound block number
            tolerance: Acceptable timestamp difference in seconds

        Returns:
            Block number closest to target timestamp
        """
        while low < high - 1:
            mid = (low + high) // 2
            block = self.w3.eth.get_block(mid)
            block_timestamp = block['timestamp']

            if abs(block_timestamp - target_timestamp) <= tolerance:
                return mid
            elif block_timestamp < target_timestamp:
                low = mid
            else:
                high = mid

        return low

    def transform_daily_blocks(self, blocks: List[Dict]) -> Dict:
        """
        Transform blocks into daily statistics

        Args:
            blocks: List of block dictionaries

        Returns:
            Dictionary with daily block statistics
        """
        if not blocks:
            return {}

        # Extract data
        block_numbers = [b['number'] for b in blocks]
        timestamps = [b['timestamp'] for b in blocks]
        transaction_counts = [len(b.get('transactions', [])) for b in blocks]
        gas_used = [b['gasUsed'] for b in blocks]
        gas_limits = [b['gasLimit'] for b in blocks]
        miners = [b.get('miner', '0x0') for b in blocks]

        # Calculate block times
        block_times = []
        for i in range(1, len(blocks)):
            time_diff = timestamps[i] - timestamps[i-1]
            if time_diff > 0:  # Avoid division by zero
                block_times.append(time_diff)

        # Calculate statistics
        total_gas_used = sum(gas_used)
        total_gas_limit = sum(gas_limits)

        stats = {
            'date': datetime.fromtimestamp(timestamps[0]).date(),
            'block_count': len(blocks),
            'avg_block_time': statistics.mean(block_times) if block_times else 0,
            'min_block_number': min(block_numbers),
            'max_block_number': max(block_numbers),
            'total_transactions': sum(transaction_counts),
            'avg_transactions_per_block': statistics.mean(transaction_counts),
            'total_gas_used': total_gas_used,
            'avg_gas_used': statistics.mean(gas_used),
            'total_gas_limit': total_gas_limit,
            'avg_gas_limit': statistics.mean(gas_limits),
            'gas_usage_percentage': (total_gas_used / total_gas_limit * 100) if total_gas_limit > 0 else 0,
            'unique_miners': len(set(miners))
        }

        return stats

    def transform_daily_transactions(self, blocks: List[Dict]) -> Dict:
        """
        Transform transactions into daily statistics

        Args:
            blocks: List of block dictionaries with full transactions

        Returns:
            Dictionary with daily transaction statistics
        """
        if not blocks:
            return {}

        # Extract all transactions
        all_transactions = []
        for block in blocks:
            all_transactions.extend(block.get('transactions', []))

        if not all_transactions:
            return {}

        # Extract transaction data
        gas_prices = []
        values = []
        gas_used_list = []
        contract_creations = 0
        contract_calls = 0
        failed_count = 0

        for tx in all_transactions:
            if isinstance(tx, dict):
                gas_prices.append(tx.get('gasPrice', 0))
                values.append(self.w3.from_wei(tx.get('value', 0), 'ether'))

                # Check if contract creation or call
                to_address = tx.get('to')
                if to_address is None:
                    contract_creations += 1
                elif to_address:
                    # Try to get receipt to check if it's a contract call
                    try:
                        receipt = self.w3.eth.get_transaction_receipt(tx['hash'])
                        gas_used_list.append(receipt['gasUsed'])

                        if receipt['status'] == 0:
                            failed_count += 1

                        # Check if contract interaction
                        if receipt.get('contractAddress'):
                            contract_creations += 1
                        elif len(tx.get('input', '0x')) > 2:
                            contract_calls += 1
                    except Exception:
                        pass

        # Convert gas prices to Gwei
        gas_prices_gwei = [self.w3.from_wei(gp, 'gwei') for gp in gas_prices if gp > 0]

        stats = {
            'date': datetime.fromtimestamp(blocks[0]['timestamp']).date(),
            'transaction_count': len(all_transactions),
            'avg_gas_price': statistics.mean(gas_prices_gwei) if gas_prices_gwei else 0,
            'median_gas_price': statistics.median(gas_prices_gwei) if gas_prices_gwei else 0,
            'min_gas_price': min(gas_prices) if gas_prices else 0,
            'max_gas_price': max(gas_prices) if gas_prices else 0,
            'avg_transaction_value': statistics.mean(values) if values else 0,
            'total_transaction_value': sum(values),
            'failed_transactions': failed_count,
            'success_rate': ((len(all_transactions) - failed_count) / len(all_transactions) * 100) if all_transactions else 0,
            'avg_gas_used': statistics.mean(gas_used_list) if gas_used_list else 0,
            'contract_creations': contract_creations,
            'contract_calls': contract_calls
        }

        return stats

    def transform_hourly_blocks(self, blocks: List[Dict]) -> List[Dict]:
        """
        Transform blocks into hourly statistics

        Args:
            blocks: List of block dictionaries

        Returns:
            List of dictionaries with hourly block statistics
        """
        if not blocks:
            return []

        # Group blocks by hour
        hourly_groups = defaultdict(list)

        for block in blocks:
            dt = datetime.fromtimestamp(block['timestamp'])
            hour_key = dt.replace(minute=0, second=0, microsecond=0)
            hourly_groups[hour_key].append(block)

        # Calculate stats for each hour
        hourly_stats = []

        for hour_dt, hour_blocks in sorted(hourly_groups.items()):
            timestamps = [b['timestamp'] for b in hour_blocks]
            transaction_counts = [len(b.get('transactions', [])) for b in hour_blocks]
            gas_used = [b['gasUsed'] for b in hour_blocks]
            miners = [b.get('miner', '0x0') for b in hour_blocks]

            # Calculate block times
            block_times = []
            for i in range(1, len(hour_blocks)):
                time_diff = timestamps[i] - timestamps[i-1]
                if time_diff > 0:
                    block_times.append(time_diff)

            stats = {
                'datetime': hour_dt,
                'hour': hour_dt.hour,
                'date': hour_dt.date(),
                'block_count': len(hour_blocks),
                'avg_block_time': statistics.mean(block_times) if block_times else 0,
                'total_transactions': sum(transaction_counts),
                'total_gas_used': sum(gas_used),
                'avg_gas_used': statistics.mean(gas_used),
                'unique_miners': len(set(miners))
            }

            hourly_stats.append(stats)

        return hourly_stats

    def transform_daily_miners(self, blocks: List[Dict]) -> List[Dict]:
        """
        Transform blocks into daily miner statistics

        Args:
            blocks: List of block dictionaries

        Returns:
            List of dictionaries with daily miner statistics
        """
        if not blocks:
            return []

        # Group by miner
        miner_stats = defaultdict(lambda: {
            'blocks_mined': 0,
            'total_gas_collected': 0,
            'total_transactions': 0
        })

        for block in blocks:
            miner = block.get('miner', '0x0')
            miner_stats[miner]['blocks_mined'] += 1
            miner_stats[miner]['total_gas_collected'] += block['gasUsed']
            miner_stats[miner]['total_transactions'] += len(block.get('transactions', []))

        # Convert to list
        date = datetime.fromtimestamp(blocks[0]['timestamp']).date()
        result = []

        for miner, stats in miner_stats.items():
            result.append({
                'date': date,
                'miner': miner,
                'blocks_mined': stats['blocks_mined'],
                'total_gas_collected': stats['total_gas_collected'],
                'total_transactions': stats['total_transactions']
            })

        # Sort by blocks mined
        result.sort(key=lambda x: x['blocks_mined'], reverse=True)

        return result

    def load_daily_blocks(self, stats: Dict):
        """Load daily block statistics into ClickHouse"""
        if not stats:
            print("⚠️  No block stats to load")
            return

        query = """
        INSERT INTO daily_blocks (
            date, block_count, avg_block_time, min_block_number, max_block_number,
            total_transactions, avg_transactions_per_block, total_gas_used,
            avg_gas_used, total_gas_limit, avg_gas_limit, gas_usage_percentage,
            unique_miners
        ) VALUES
        """

        self.ch_client.execute(query, [tuple(stats.values())])
        print(f"✅ Loaded daily block stats for {stats['date']}")

    def load_daily_transactions(self, stats: Dict):
        """Load daily transaction statistics into ClickHouse"""
        if not stats:
            print("⚠️  No transaction stats to load")
            return

        query = """
        INSERT INTO daily_transactions (
            date, transaction_count, avg_gas_price, median_gas_price,
            min_gas_price, max_gas_price, avg_transaction_value,
            total_transaction_value, failed_transactions, success_rate,
            avg_gas_used, contract_creations, contract_calls
        ) VALUES
        """

        self.ch_client.execute(query, [tuple(stats.values())])
        print(f"✅ Loaded daily transaction stats for {stats['date']}")

    def load_hourly_blocks(self, stats_list: List[Dict]):
        """Load hourly block statistics into ClickHouse"""
        if not stats_list:
            print("⚠️  No hourly stats to load")
            return

        query = """
        INSERT INTO hourly_blocks (
            datetime, hour, date, block_count, avg_block_time,
            total_transactions, total_gas_used, avg_gas_used, unique_miners
        ) VALUES
        """

        data = [tuple(stats.values()) for stats in stats_list]
        self.ch_client.execute(query, data)
        print(f"✅ Loaded {len(stats_list)} hourly block stats")

    def load_daily_miners(self, stats_list: List[Dict]):
        """Load daily miner statistics into ClickHouse"""
        if not stats_list:
            print("⚠️  No miner stats to load")
            return

        query = """
        INSERT INTO daily_miners (
            date, miner, blocks_mined, total_gas_collected, total_transactions
        ) VALUES
        """

        data = [tuple(stats.values()) for stats in stats_list]
        self.ch_client.execute(query, data)
        print(f"✅ Loaded {len(stats_list)} miner stats")

    def run_etl_for_date(self, target_date: datetime):
        """
        Run complete ETL pipeline for a specific date

        Args:
            target_date: Date to process
        """
        print(f"\n{'='*60}")
        print(f"🚀 Starting ETL for {target_date.date()}")
        print(f"{'='*60}\n")

        # Extract
        print("1️⃣  EXTRACT: Fetching blocks...")
        blocks = self.get_blocks_by_date(target_date, include_transactions=True)

        if not blocks:
            print("❌ No blocks found for this date")
            return

        print(f"✅ Fetched {len(blocks)} blocks\n")

        # Transform
        print("2️⃣  TRANSFORM: Processing data...")

        daily_blocks_stats = self.transform_daily_blocks(blocks)
        print(f"  ✓ Daily block stats calculated")

        daily_tx_stats = self.transform_daily_transactions(blocks)
        print(f"  ✓ Daily transaction stats calculated")

        hourly_stats = self.transform_hourly_blocks(blocks)
        print(f"  ✓ Hourly stats calculated ({len(hourly_stats)} hours)")

        miner_stats = self.transform_daily_miners(blocks)
        print(f"  ✓ Miner stats calculated ({len(miner_stats)} miners)")

        print("✅ Transformation complete\n")

        # Load
        print("3️⃣  LOAD: Inserting into ClickHouse...")

        self.load_daily_blocks(daily_blocks_stats)
        self.load_daily_transactions(daily_tx_stats)
        self.load_hourly_blocks(hourly_stats)
        self.load_daily_miners(miner_stats)

        print(f"\n{'='*60}")
        print(f"✅ ETL Complete for {target_date.date()}")
        print(f"{'='*60}\n")

    def run_etl_for_range(self, start_date: datetime, end_date: datetime):
        """
        Run ETL for a date range

        Args:
            start_date: Start date
            end_date: End date (inclusive)
        """
        current_date = start_date

        while current_date <= end_date:
            try:
                self.run_etl_for_date(current_date)
            except Exception as e:
                print(f"❌ Error processing {current_date.date()}: {e}")

            current_date += timedelta(days=1)


def main():
    """Main entry point"""
    # Configuration from environment
    rpc_url = os.getenv('RPC_URL', 'http://localhost:8545')
    ch_host = os.getenv('CLICKHOUSE_HOST', 'localhost')
    ch_port = int(os.getenv('CLICKHOUSE_PORT', '9000'))
    ch_user = os.getenv('CLICKHOUSE_USER', 'default')
    ch_pass = os.getenv('CLICKHOUSE_PASSWORD', '')
    ch_db = os.getenv('CLICKHOUSE_DATABASE', 'blockchain_analytics')

    # Create ETL instance
    etl = BlockchainETL(
        rpc_url=rpc_url,
        clickhouse_host=ch_host,
        clickhouse_port=ch_port,
        clickhouse_user=ch_user,
        clickhouse_password=ch_pass,
        clickhouse_database=ch_db
    )

    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python blockchain_etl.py today")
        print("  python blockchain_etl.py yesterday")
        print("  python blockchain_etl.py YYYY-MM-DD")
        print("  python blockchain_etl.py YYYY-MM-DD YYYY-MM-DD (date range)")
        sys.exit(1)

    arg1 = sys.argv[1].lower()

    if arg1 == 'today':
        target_date = datetime.now()
        etl.run_etl_for_date(target_date)
    elif arg1 == 'yesterday':
        target_date = datetime.now() - timedelta(days=1)
        etl.run_etl_for_date(target_date)
    else:
        try:
            start_date = datetime.strptime(sys.argv[1], '%Y-%m-%d')

            if len(sys.argv) >= 3:
                end_date = datetime.strptime(sys.argv[2], '%Y-%m-%d')
                etl.run_etl_for_range(start_date, end_date)
            else:
                etl.run_etl_for_date(start_date)
        except ValueError:
            print("❌ Invalid date format. Use YYYY-MM-DD")
            sys.exit(1)


if __name__ == '__main__':
    main()
