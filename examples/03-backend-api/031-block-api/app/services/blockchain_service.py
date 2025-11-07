"""
Blockchain service for interacting with Ethereum nodes
"""
from web3 import Web3
from web3.exceptions import BlockNotFound, TransactionNotFound
from typing import Optional, List, Dict, Any
from ..core.config import settings


class BlockchainService:
    """Service for blockchain interactions"""

    def __init__(self):
        """Initialize Web3 connection"""
        self.w3 = Web3(Web3.HTTPProvider(settings.RPC_URL))

        if not self.w3.is_connected():
            raise ConnectionError(f"Cannot connect to blockchain node at {settings.RPC_URL}")

    # ==================== Connection & Health ====================

    def is_connected(self) -> bool:
        """Check if connected to node"""
        return self.w3.is_connected()

    def get_chain_id(self) -> int:
        """Get chain ID"""
        return self.w3.eth.chain_id

    # ==================== Block Operations ====================

    def get_latest_block_number(self) -> int:
        """Get latest block number"""
        return self.w3.eth.block_number

    def get_block(self, block_identifier: int | str, full_transactions: bool = False) -> Optional[Dict]:
        """
        Get block by number or hash

        Args:
            block_identifier: Block number or hash
            full_transactions: Return full transaction objects

        Returns:
            Block data dict or None
        """
        try:
            block = self.w3.eth.get_block(block_identifier, full_transactions=full_transactions)
            return self._format_block(block, full_transactions)
        except BlockNotFound:
            return None

    def get_blocks(
        self,
        start_block: Optional[int] = None,
        limit: int = 20,
        descending: bool = True
    ) -> List[Dict]:
        """
        Get multiple blocks

        Args:
            start_block: Starting block number (default: latest)
            limit: Number of blocks to fetch
            descending: Fetch in descending order

        Returns:
            List of block data dicts
        """
        if start_block is None:
            start_block = self.get_latest_block_number()

        blocks = []
        for i in range(limit):
            block_num = start_block - i if descending else start_block + i

            if block_num < 0:
                break

            try:
                block = self.get_block(block_num)
                if block:
                    blocks.append(block)
            except Exception:
                continue

        return blocks

    def _format_block(self, block: Any, full_transactions: bool = False) -> Dict:
        """Format block data"""
        return {
            "number": block['number'],
            "hash": block['hash'].hex(),
            "parentHash": block['parentHash'].hex(),
            "timestamp": block['timestamp'],
            "miner": block['miner'],
            "difficulty": block['difficulty'],
            "totalDifficulty": block.get('totalDifficulty', 0),
            "size": block['size'],
            "gasLimit": block['gasLimit'],
            "gasUsed": block['gasUsed'],
            "transactionCount": len(block['transactions']),
            "nonce": block['nonce'].hex() if block.get('nonce') else "0x0",
            "extraData": block.get('extraData', b'').hex(),
            "transactions": [
                tx['hash'].hex() if isinstance(tx, dict) else tx.hex()
                for tx in block['transactions']
            ] if not full_transactions else [
                self._format_transaction(tx) for tx in block['transactions']
            ],
            "baseFeePerGas": block.get('baseFeePerGas'),
        }

    # ==================== Transaction Operations ====================

    def get_transaction(self, tx_hash: str) -> Optional[Dict]:
        """
        Get transaction by hash

        Args:
            tx_hash: Transaction hash

        Returns:
            Transaction data dict or None
        """
        try:
            tx = self.w3.eth.get_transaction(tx_hash)
            return self._format_transaction(tx)
        except TransactionNotFound:
            return None

    def get_transaction_receipt(self, tx_hash: str) -> Optional[Dict]:
        """
        Get transaction receipt

        Args:
            tx_hash: Transaction hash

        Returns:
            Receipt data dict or None
        """
        try:
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            return self._format_receipt(receipt)
        except TransactionNotFound:
            return None

    def get_pending_transaction_count(self) -> int:
        """Get number of pending transactions"""
        try:
            pending_block = self.w3.eth.get_block('pending')
            return len(pending_block['transactions'])
        except Exception:
            return 0

    def _format_transaction(self, tx: Any) -> Dict:
        """Format transaction data"""
        return {
            "hash": tx['hash'].hex(),
            "blockNumber": tx.get('blockNumber'),
            "from": tx['from'],
            "to": tx.get('to'),
            "value": str(tx['value']),
            "gas": tx['gas'],
            "gasPrice": tx.get('gasPrice', 0),
            "nonce": tx['nonce'],
            "transactionIndex": tx.get('transactionIndex'),
            "input": tx['input'].hex() if isinstance(tx.get('input'), bytes) else tx.get('input', ''),
            "blockHash": tx.get('blockHash', b'').hex() if tx.get('blockHash') else None,
            "v": tx.get('v'),
            "r": tx.get('r', b'').hex() if tx.get('r') else None,
            "s": tx.get('s', b'').hex() if tx.get('s') else None,
        }

    def _format_receipt(self, receipt: Any) -> Dict:
        """Format transaction receipt"""
        return {
            "transactionHash": receipt['transactionHash'].hex(),
            "blockNumber": receipt['blockNumber'],
            "blockHash": receipt['blockHash'].hex(),
            "from": receipt['from'],
            "to": receipt.get('to'),
            "gasUsed": receipt['gasUsed'],
            "cumulativeGasUsed": receipt['cumulativeGasUsed'],
            "effectiveGasPrice": receipt.get('effectiveGasPrice'),
            "status": receipt['status'],
            "logs": [self._format_log(log) for log in receipt['logs']],
            "contractAddress": receipt.get('contractAddress'),
        }

    def _format_log(self, log: Any) -> Dict:
        """Format log entry"""
        return {
            "address": log['address'],
            "topics": [topic.hex() for topic in log['topics']],
            "data": log['data'].hex() if isinstance(log['data'], bytes) else log['data'],
            "blockNumber": log['blockNumber'],
            "transactionHash": log['transactionHash'].hex(),
            "logIndex": log['logIndex'],
        }

    # ==================== Address Operations ====================

    def get_balance(self, address: str) -> int:
        """
        Get address balance in Wei

        Args:
            address: Ethereum address

        Returns:
            Balance in Wei
        """
        try:
            return self.w3.eth.get_balance(address)
        except Exception:
            return 0

    def get_transaction_count(self, address: str) -> int:
        """
        Get transaction count for address

        Args:
            address: Ethereum address

        Returns:
            Transaction count (nonce)
        """
        try:
            return self.w3.eth.get_transaction_count(address)
        except Exception:
            return 0

    def get_code(self, address: str) -> str:
        """
        Get contract code at address

        Args:
            address: Ethereum address

        Returns:
            Contract bytecode (hex)
        """
        try:
            code = self.w3.eth.get_code(address)
            return code.hex()
        except Exception:
            return "0x"

    def is_contract(self, address: str) -> bool:
        """
        Check if address is a contract

        Args:
            address: Ethereum address

        Returns:
            True if contract, False otherwise
        """
        code = self.get_code(address)
        return code != "0x" and code != "0x0"

    # ==================== Statistics ====================

    def get_gas_price(self) -> int:
        """Get current gas price in Wei"""
        try:
            return self.w3.eth.gas_price
        except Exception:
            return 0

    def get_stats(self) -> Dict:
        """Get blockchain statistics"""
        latest_block_num = self.get_latest_block_number()
        latest_block = self.get_block(latest_block_num)

        # Calculate average block time (last 100 blocks)
        avg_block_time = self._calculate_avg_block_time()

        return {
            "latest_block": latest_block_num,
            "difficulty": latest_block.get('difficulty', 0) if latest_block else 0,
            "avg_block_time": avg_block_time,
            "avg_gas_price": self.get_gas_price(),
            "pending_transactions": self.get_pending_transaction_count(),
        }

    def _calculate_avg_block_time(self, sample_size: int = 100) -> float:
        """Calculate average block time"""
        try:
            latest = self.get_latest_block_number()
            if latest < sample_size:
                sample_size = latest

            latest_block = self.w3.eth.get_block(latest)
            old_block = self.w3.eth.get_block(latest - sample_size)

            time_diff = latest_block['timestamp'] - old_block['timestamp']
            return time_diff / sample_size
        except Exception:
            return 12.0  # Default Ethereum block time

    # ==================== Utility Functions ====================

    def wei_to_eth(self, wei: int) -> float:
        """Convert Wei to ETH"""
        return self.w3.from_wei(wei, 'ether')

    def eth_to_wei(self, eth: float) -> int:
        """Convert ETH to Wei"""
        return self.w3.to_wei(eth, 'ether')


# Create global instance
blockchain_service = BlockchainService()
