#!/usr/bin/env python3
"""
Send ETH Transaction Example
ส่ง ETH จาก address หนึ่งไปยังอีก address พร้อม gas estimation
"""

import os
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv
from typing import Optional, Dict
from decimal import Decimal

# Load environment variables
load_dotenv()

class EthSender:
    """Class สำหรับส่ง ETH transactions"""

    def __init__(self, rpc_url: Optional[str] = None):
        """
        Initialize ETH sender

        Args:
            rpc_url: RPC endpoint URL
        """
        self.rpc_url = rpc_url or os.getenv('RPC_URL', 'http://localhost:8545')
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))

        if not self.w3.is_connected():
            raise ConnectionError(f"Failed to connect to {self.rpc_url}")

    def create_account(self) -> Dict[str, str]:
        """
        สร้าง account ใหม่

        Returns:
            Dictionary containing address and private_key
        """
        account = Account.create()
        return {
            'address': account.address,
            'private_key': account.key.hex()
        }

    def get_balance(self, address: str) -> Decimal:
        """
        ดู balance (in ETH)

        Args:
            address: Ethereum address

        Returns:
            Balance in ETH
        """
        balance_wei = self.w3.eth.get_balance(address)
        return Decimal(str(self.w3.from_wei(balance_wei, 'ether')))

    def estimate_gas(
        self,
        from_address: str,
        to_address: str,
        value_eth: float
    ) -> int:
        """
        Estimate gas สำหรับ transaction

        Args:
            from_address: Sender address
            to_address: Recipient address
            value_eth: Amount in ETH

        Returns:
            Estimated gas units
        """
        value_wei = self.w3.to_wei(value_eth, 'ether')

        gas_estimate = self.w3.eth.estimate_gas({
            'from': from_address,
            'to': to_address,
            'value': value_wei
        })

        return gas_estimate

    def send_eth(
        self,
        private_key: str,
        to_address: str,
        amount_eth: float,
        gas_limit: Optional[int] = None,
        gas_price_gwei: Optional[float] = None,
        nonce: Optional[int] = None
    ) -> Dict:
        """
        ส่ง ETH transaction

        Args:
            private_key: Private key ของ sender (with or without 0x)
            to_address: Recipient address
            amount_eth: Amount to send in ETH
            gas_limit: Gas limit (optional, will estimate if not provided)
            gas_price_gwei: Gas price in Gwei (optional, will use network price if not provided)
            nonce: Transaction nonce (optional, will fetch current nonce if not provided)

        Returns:
            Transaction receipt dictionary
        """
        # 1. Load account from private key
        if not private_key.startswith('0x'):
            private_key = '0x' + private_key

        account = Account.from_key(private_key)
        from_address = account.address

        # 2. Check balance
        balance = self.get_balance(from_address)
        if balance < Decimal(str(amount_eth)):
            raise ValueError(
                f"Insufficient balance. Have {balance} ETH, need {amount_eth} ETH"
            )

        # 3. Get nonce
        if nonce is None:
            nonce = self.w3.eth.get_transaction_count(from_address)

        # 4. Estimate gas
        if gas_limit is None:
            gas_limit = self.estimate_gas(from_address, to_address, amount_eth)
            # Add 20% buffer
            gas_limit = int(gas_limit * 1.2)

        # 5. Get gas price
        if gas_price_gwei is None:
            gas_price_wei = self.w3.eth.gas_price
        else:
            gas_price_wei = self.w3.to_wei(gas_price_gwei, 'gwei')

        # 6. Calculate total cost
        value_wei = self.w3.to_wei(amount_eth, 'ether')
        total_cost_wei = value_wei + (gas_limit * gas_price_wei)
        total_cost_eth = self.w3.from_wei(total_cost_wei, 'ether')

        if balance < Decimal(str(total_cost_eth)):
            raise ValueError(
                f"Insufficient balance for gas. Need {total_cost_eth} ETH (including gas), "
                f"have {balance} ETH"
            )

        # 7. Build transaction
        transaction = {
            'nonce': nonce,
            'to': to_address,
            'value': value_wei,
            'gas': gas_limit,
            'gasPrice': gas_price_wei,
            'chainId': self.w3.eth.chain_id
        }

        # 8. Sign transaction
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)

        # 9. Send transaction
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        print(f"📤 Transaction sent!")
        print(f"   Hash: {tx_hash.hex()}")
        print(f"   Waiting for confirmation...")

        # 10. Wait for receipt
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        # 11. Return result
        return {
            'hash': tx_hash.hex(),
            'from': from_address,
            'to': to_address,
            'value_eth': amount_eth,
            'gas_used': receipt['gasUsed'],
            'gas_price_gwei': self.w3.from_wei(gas_price_wei, 'gwei'),
            'total_cost_eth': float(self.w3.from_wei(
                receipt['gasUsed'] * gas_price_wei + value_wei,
                'ether'
            )),
            'block_number': receipt['blockNumber'],
            'status': 'success' if receipt['status'] == 1 else 'failed'
        }

    def send_eth_batch(
        self,
        private_key: str,
        recipients: list[tuple[str, float]]
    ) -> list[Dict]:
        """
        ส่ง ETH ไปหลาย addresses พร้อมกัน

        Args:
            private_key: Private key ของ sender
            recipients: List of (address, amount_eth) tuples

        Returns:
            List of transaction receipts
        """
        if not private_key.startswith('0x'):
            private_key = '0x' + private_key

        account = Account.from_key(private_key)
        from_address = account.address

        # Get starting nonce
        nonce = self.w3.eth.get_transaction_count(from_address)

        receipts = []

        for i, (to_address, amount) in enumerate(recipients):
            print(f"\n[{i+1}/{len(recipients)}] Sending {amount} ETH to {to_address}...")

            try:
                receipt = self.send_eth(
                    private_key=private_key,
                    to_address=to_address,
                    amount_eth=amount,
                    nonce=nonce + i
                )
                receipts.append(receipt)
                print(f"✅ Success! Hash: {receipt['hash'][:20]}...")

            except Exception as e:
                print(f"❌ Failed: {e}")
                receipts.append({'error': str(e)})

        return receipts


def print_separator(title: str = ""):
    """พิมพ์เส้นแบ่ง"""
    if title:
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print('=' * 60)
    else:
        print('-' * 60)


def main():
    """ฟังก์ชันหลักสำหรับตัวอย่างการใช้งาน"""

    print("💸 Send ETH Transaction Example")
    print("=" * 60)

    # 1. Initialize
    sender = EthSender()

    print(f"📡 Connected to: {sender.rpc_url}")
    print(f"   Chain ID: {sender.w3.eth.chain_id}")

    # 2. ตั้งค่า accounts (ใช้ Anvil default accounts)
    # Default account #0 (มี ETH เยอะ)
    sender_private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    sender_address = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"

    # Default account #1 (recipient)
    recipient_address = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"

    # 3. แสดง balances ก่อนส่ง
    print_separator("Balances Before")
    sender_balance = sender.get_balance(sender_address)
    recipient_balance = sender.get_balance(recipient_address)

    print(f"Sender ({sender_address[:10]}...):")
    print(f"  Balance: {sender_balance} ETH")
    print(f"\nRecipient ({recipient_address[:10]}...):")
    print(f"  Balance: {recipient_balance} ETH")

    # 4. Estimate gas
    print_separator("Gas Estimation")
    amount_to_send = 1.5  # ETH

    try:
        estimated_gas = sender.estimate_gas(sender_address, recipient_address, amount_to_send)
        gas_price_wei = sender.w3.eth.gas_price
        gas_price_gwei = sender.w3.from_wei(gas_price_wei, 'gwei')

        print(f"Amount to send: {amount_to_send} ETH")
        print(f"Estimated gas: {estimated_gas:,} units")
        print(f"Gas price: {gas_price_gwei} Gwei")

        total_gas_cost_eth = sender.w3.from_wei(estimated_gas * gas_price_wei, 'ether')
        print(f"Estimated gas cost: {total_gas_cost_eth} ETH")
        print(f"Total cost: {amount_to_send + float(total_gas_cost_eth):.6f} ETH")

    except Exception as e:
        print(f"❌ Gas estimation failed: {e}")
        return

    # 5. ส่ง transaction
    print_separator("Sending Transaction")

    try:
        receipt = sender.send_eth(
            private_key=sender_private_key,
            to_address=recipient_address,
            amount_eth=amount_to_send
        )

        print(f"\n✅ Transaction successful!")
        print(f"   Hash: {receipt['hash']}")
        print(f"   Block: {receipt['block_number']}")
        print(f"   Gas used: {receipt['gas_used']:,} units")
        print(f"   Gas price: {receipt['gas_price_gwei']:.2f} Gwei")
        print(f"   Total cost: {receipt['total_cost_eth']:.6f} ETH")

    except Exception as e:
        print(f"❌ Transaction failed: {e}")
        return

    # 6. แสดง balances หลังส่ง
    print_separator("Balances After")
    sender_balance_after = sender.get_balance(sender_address)
    recipient_balance_after = sender.get_balance(recipient_address)

    print(f"Sender ({sender_address[:10]}...):")
    print(f"  Before:  {sender_balance} ETH")
    print(f"  After:   {sender_balance_after} ETH")
    print(f"  Change:  {sender_balance_after - sender_balance:+.6f} ETH")

    print(f"\nRecipient ({recipient_address[:10]}...):")
    print(f"  Before:  {recipient_balance} ETH")
    print(f"  After:   {recipient_balance_after} ETH")
    print(f"  Change:  {recipient_balance_after - recipient_balance:+.6f} ETH")

    # 7. ตัวอย่าง batch send (ถ้าต้องการ)
    print_separator("Batch Send Example")
    print("💡 To send to multiple addresses, use:")
    print("""
    recipients = [
        ("0x70997970C51812dc3A010C7d01b50e0d17dc79C8", 0.1),
        ("0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC", 0.2),
        ("0x90F79bf6EB2c4f870365E785982E1f101E93b906", 0.3),
    ]
    receipts = sender.send_eth_batch(sender_private_key, recipients)
    """)

    print_separator()
    print("✅ All examples completed!")
    print("\n💡 Next steps:")
    print("  - Try changing the amount")
    print("  - Try sending to your own addresses")
    print("  - Check 018-erc20-interact for token transfers")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
