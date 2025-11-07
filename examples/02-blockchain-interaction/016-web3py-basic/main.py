#!/usr/bin/env python3
"""
Web3.py Basic Connection Example
เชื่อมต่อกับ Ethereum node และดึงข้อมูลพื้นฐาน
"""

import os
from web3 import Web3
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

class Web3Connection:
    """Class สำหรับจัดการการเชื่อมต่อกับ Ethereum node"""

    def __init__(self, rpc_url: Optional[str] = None):
        """
        Initialize Web3 connection

        Args:
            rpc_url: RPC endpoint URL (default: from .env or localhost)
        """
        self.rpc_url = rpc_url or os.getenv('RPC_URL', 'http://localhost:8545')
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))

    def is_connected(self) -> bool:
        """ตรวจสอบว่าเชื่อมต่อสำเร็จหรือไม่"""
        return self.w3.is_connected()

    def get_chain_id(self) -> int:
        """ดึง chain ID"""
        return self.w3.eth.chain_id

    def get_latest_block_number(self) -> int:
        """ดึง block number ล่าสุด"""
        return self.w3.eth.block_number

    def get_block(self, block_identifier: int | str = 'latest') -> dict:
        """
        ดึงข้อมูล block

        Args:
            block_identifier: Block number หรือ 'latest'

        Returns:
            Block information dictionary
        """
        block = self.w3.eth.get_block(block_identifier)
        return {
            'number': block['number'],
            'hash': block['hash'].hex(),
            'parent_hash': block['parentHash'].hex(),
            'timestamp': block['timestamp'],
            'miner': block['miner'],
            'gas_limit': block['gasLimit'],
            'gas_used': block['gasUsed'],
            'transaction_count': len(block['transactions']),
            'base_fee_per_gas': block.get('baseFeePerGas'),
        }

    def get_transaction(self, tx_hash: str) -> dict:
        """
        ดึงข้อมูล transaction

        Args:
            tx_hash: Transaction hash (with or without 0x prefix)

        Returns:
            Transaction information dictionary
        """
        if not tx_hash.startswith('0x'):
            tx_hash = '0x' + tx_hash

        tx = self.w3.eth.get_transaction(tx_hash)

        return {
            'hash': tx['hash'].hex(),
            'from': tx['from'],
            'to': tx['to'],
            'value': self.w3.from_wei(tx['value'], 'ether'),
            'gas': tx['gas'],
            'gas_price': self.w3.from_wei(tx['gasPrice'], 'gwei') if tx.get('gasPrice') else None,
            'nonce': tx['nonce'],
            'block_number': tx['blockNumber'],
        }

    def get_balance(self, address: str) -> float:
        """
        ดู balance ของ address (in ETH)

        Args:
            address: Ethereum address

        Returns:
            Balance in ETH
        """
        if not self.w3.is_address(address):
            raise ValueError(f"Invalid address: {address}")

        balance_wei = self.w3.eth.get_balance(address)
        return self.w3.from_wei(balance_wei, 'ether')

    def get_transaction_count(self, address: str) -> int:
        """
        ดู transaction count (nonce) ของ address

        Args:
            address: Ethereum address

        Returns:
            Transaction count
        """
        return self.w3.eth.get_transaction_count(address)

    def get_gas_price(self) -> float:
        """ดู gas price ปัจจุบัน (in Gwei)"""
        gas_price_wei = self.w3.eth.gas_price
        return self.w3.from_wei(gas_price_wei, 'gwei')

    def to_wei(self, amount: float, unit: str = 'ether') -> int:
        """แปลงจาก ether/gwei เป็น wei"""
        return self.w3.to_wei(amount, unit)

    def from_wei(self, amount: int, unit: str = 'ether') -> float:
        """แปลงจาก wei เป็น ether/gwei"""
        return self.w3.from_wei(amount, unit)

    def is_address(self, address: str) -> bool:
        """ตรวจสอบว่า address ถูกต้องหรือไม่"""
        return self.w3.is_address(address)

    def to_checksum_address(self, address: str) -> str:
        """แปลง address เป็น checksum format"""
        return self.w3.to_checksum_address(address)


def print_separator(title: str = ""):
    """พิมพ์เส้นแบ่ง"""
    if title:
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print('=' * 60)
    else:
        print('-' * 60)


def main():
    """ฟังก์ชันหลักสำหรับทดสอบ Web3 connection"""

    print("🔗 Web3.py Basic Connection Example")
    print("=" * 60)

    # 1. สร้าง connection
    web3 = Web3Connection()

    # 2. ตรวจสอบการเชื่อมต่อ
    print(f"\n📡 Connecting to: {web3.rpc_url}")

    if not web3.is_connected():
        print("❌ Failed to connect to Ethereum node")
        print("\n💡 Make sure you have a node running:")
        print("   - Anvil: anvil")
        print("   - Ganache: ganache-cli")
        print("   - Or set RPC_URL in .env file")
        return

    print("✅ Connected successfully!")

    # 3. แสดงข้อมูล network
    print_separator("Network Information")
    print(f"Chain ID: {web3.get_chain_id()}")
    print(f"Latest Block: {web3.get_latest_block_number():,}")
    print(f"Gas Price: {web3.get_gas_price():.2f} Gwei")

    # 4. แสดงข้อมูล latest block
    print_separator("Latest Block Details")
    latest_block = web3.get_block('latest')
    print(f"Block Number: {latest_block['number']:,}")
    print(f"Block Hash: {latest_block['hash']}")
    print(f"Timestamp: {latest_block['timestamp']}")
    print(f"Miner: {latest_block['miner']}")
    print(f"Gas Used: {latest_block['gas_used']:,} / {latest_block['gas_limit']:,}")
    print(f"Transactions: {latest_block['transaction_count']}")
    if latest_block['base_fee_per_gas']:
        base_fee_gwei = web3.from_wei(latest_block['base_fee_per_gas'], 'gwei')
        print(f"Base Fee: {base_fee_gwei:.2f} Gwei")

    # 5. ตรวจสอบ balance ของ account แรก (ถ้ามี)
    print_separator("Account Information")

    # ใช้ default account จาก Anvil/Ganache
    test_accounts = [
        "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266",  # Anvil default account #0
        "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",  # Anvil default account #1
    ]

    for i, address in enumerate(test_accounts, 1):
        try:
            balance = web3.get_balance(address)
            tx_count = web3.get_transaction_count(address)
            print(f"\nAccount #{i}:")
            print(f"  Address: {address}")
            print(f"  Balance: {balance:.4f} ETH")
            print(f"  Transactions: {tx_count}")
        except Exception as e:
            print(f"\nAccount #{i}: Unable to fetch (node may not have this account)")
            break

    # 6. ตัวอย่างการใช้ utility functions
    print_separator("Utility Functions")

    # Wei conversion
    amount_eth = 1.5
    amount_wei = web3.to_wei(amount_eth, 'ether')
    print(f"{amount_eth} ETH = {amount_wei:,} Wei")

    amount_gwei = 50
    amount_wei_from_gwei = web3.to_wei(amount_gwei, 'gwei')
    print(f"{amount_gwei} Gwei = {amount_wei_from_gwei:,} Wei")

    # Back to ether
    back_to_eth = web3.from_wei(amount_wei, 'ether')
    print(f"{amount_wei:,} Wei = {back_to_eth} ETH")

    # Address validation
    print("\nAddress Validation:")
    valid_addr = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
    invalid_addr = "0xinvalid"

    print(f"  {valid_addr[:20]}... is valid: {web3.is_address(valid_addr)}")
    print(f"  {invalid_addr} is valid: {web3.is_address(invalid_addr)}")

    # Checksum address
    lowercase_addr = valid_addr.lower()
    checksum_addr = web3.to_checksum_address(lowercase_addr)
    print(f"\nChecksum conversion:")
    print(f"  From: {lowercase_addr}")
    print(f"  To:   {checksum_addr}")

    print_separator()
    print("✅ All examples completed successfully!")
    print("\n💡 Next steps:")
    print("  - Try 017-send-eth to send transactions")
    print("  - Try 018-erc20-interact to interact with tokens")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
