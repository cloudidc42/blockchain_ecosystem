#!/usr/bin/env python3
"""
ERC-20 Token Interaction Example
โต้ตอบกับ ERC-20 tokens: transfer, approve, balance checking
"""

import os
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv
from typing import Optional, Dict, List, Tuple
from decimal import Decimal

# Load environment variables
load_dotenv()

# ERC-20 ABI (only functions we need)
ERC20_ABI = [
    # Read functions
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {"name": "owner", "type": "address"},
            {"name": "spender", "type": "address"}
        ],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    },
    # Write functions
    {
        "constant": False,
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "spender", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "from", "type": "address"},
            {"name": "to", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "transferFrom",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    },
    # Events
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "from", "type": "address"},
            {"indexed": True, "name": "to", "type": "address"},
            {"indexed": False, "name": "value", "type": "uint256"}
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "owner", "type": "address"},
            {"indexed": True, "name": "spender", "type": "address"},
            {"indexed": False, "name": "value", "type": "uint256"}
        ],
        "name": "Approval",
        "type": "event"
    }
]


class ERC20Interact:
    """Class สำหรับโต้ตอบกับ ERC-20 token contracts"""

    def __init__(self, rpc_url: Optional[str] = None):
        """
        Initialize ERC-20 interaction

        Args:
            rpc_url: RPC endpoint URL (default: from .env or localhost)
        """
        self.rpc_url = rpc_url or os.getenv('RPC_URL', 'http://localhost:8545')
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))

        if not self.w3.is_connected():
            raise ConnectionError(f"Cannot connect to {self.rpc_url}")

    def get_contract(self, token_address: str):
        """
        Get contract instance

        Args:
            token_address: ERC-20 token contract address

        Returns:
            Contract instance
        """
        if not self.w3.is_address(token_address):
            raise ValueError(f"Invalid token address: {token_address}")

        checksum_address = self.w3.to_checksum_address(token_address)
        return self.w3.eth.contract(address=checksum_address, abi=ERC20_ABI)

    # ==================== Read Functions ====================

    def get_token_info(self, token_address: str) -> Dict:
        """
        Get token metadata

        Args:
            token_address: Token contract address

        Returns:
            Dictionary with name, symbol, decimals, totalSupply
        """
        contract = self.get_contract(token_address)

        try:
            name = contract.functions.name().call()
            symbol = contract.functions.symbol().call()
            decimals = contract.functions.decimals().call()
            total_supply = contract.functions.totalSupply().call()

            return {
                'address': token_address,
                'name': name,
                'symbol': symbol,
                'decimals': decimals,
                'total_supply': total_supply,
                'total_supply_formatted': self._format_amount(total_supply, decimals),
            }
        except Exception as e:
            raise RuntimeError(f"Failed to get token info: {e}")

    def get_balance(
        self,
        token_address: str,
        account_address: str,
        formatted: bool = True
    ) -> float | int:
        """
        Get token balance of an account

        Args:
            token_address: Token contract address
            account_address: Account to check balance
            formatted: Return formatted balance (divided by decimals)

        Returns:
            Token balance
        """
        contract = self.get_contract(token_address)
        balance = contract.functions.balanceOf(account_address).call()

        if formatted:
            decimals = contract.functions.decimals().call()
            return self._format_amount(balance, decimals)

        return balance

    def get_allowance(
        self,
        token_address: str,
        owner: str,
        spender: str,
        formatted: bool = True
    ) -> float | int:
        """
        Get allowance amount

        Args:
            token_address: Token contract address
            owner: Token owner address
            spender: Spender address
            formatted: Return formatted amount

        Returns:
            Allowance amount
        """
        contract = self.get_contract(token_address)
        allowance = contract.functions.allowance(owner, spender).call()

        if formatted:
            decimals = contract.functions.decimals().call()
            return self._format_amount(allowance, decimals)

        return allowance

    # ==================== Write Functions ====================

    def transfer(
        self,
        token_address: str,
        private_key: str,
        to_address: str,
        amount: float,
        gas_limit: Optional[int] = None,
        gas_price_gwei: Optional[float] = None
    ) -> Dict:
        """
        Transfer tokens to another address

        Args:
            token_address: Token contract address
            private_key: Sender's private key
            to_address: Recipient address
            amount: Amount to transfer (in token units, not wei)
            gas_limit: Optional gas limit
            gas_price_gwei: Optional gas price in Gwei

        Returns:
            Transaction receipt
        """
        contract = self.get_contract(token_address)
        account = Account.from_key(private_key)
        from_address = account.address

        # Get decimals and convert amount
        decimals = contract.functions.decimals().call()
        amount_wei = self._parse_amount(amount, decimals)

        # Check balance
        balance = contract.functions.balanceOf(from_address).call()
        if balance < amount_wei:
            raise ValueError(
                f"Insufficient balance. Have: {self._format_amount(balance, decimals)}, "
                f"Need: {amount}"
            )

        # Build transaction
        nonce = self.w3.eth.get_transaction_count(from_address)

        # Estimate gas if not provided
        if gas_limit is None:
            try:
                gas_limit = contract.functions.transfer(
                    to_address,
                    amount_wei
                ).estimate_gas({'from': from_address})
                gas_limit = int(gas_limit * 1.2)  # Add 20% buffer
            except Exception as e:
                raise RuntimeError(f"Gas estimation failed: {e}")

        # Get gas price
        if gas_price_gwei is not None:
            gas_price = self.w3.to_wei(gas_price_gwei, 'gwei')
        else:
            gas_price = self.w3.eth.gas_price

        # Build transaction
        transaction = contract.functions.transfer(
            to_address,
            amount_wei
        ).build_transaction({
            'from': from_address,
            'nonce': nonce,
            'gas': gas_limit,
            'gasPrice': gas_price,
        })

        # Sign and send
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        print(f"⏳ Transaction sent: {tx_hash.hex()}")
        print(f"   Waiting for confirmation...")

        # Wait for receipt
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return self._format_receipt(receipt, 'transfer')

    def approve(
        self,
        token_address: str,
        private_key: str,
        spender: str,
        amount: float,
        gas_limit: Optional[int] = None,
        gas_price_gwei: Optional[float] = None
    ) -> Dict:
        """
        Approve spender to spend tokens

        Args:
            token_address: Token contract address
            private_key: Owner's private key
            spender: Spender address
            amount: Amount to approve
            gas_limit: Optional gas limit
            gas_price_gwei: Optional gas price in Gwei

        Returns:
            Transaction receipt
        """
        contract = self.get_contract(token_address)
        account = Account.from_key(private_key)
        from_address = account.address

        # Get decimals and convert amount
        decimals = contract.functions.decimals().call()
        amount_wei = self._parse_amount(amount, decimals)

        # Build transaction
        nonce = self.w3.eth.get_transaction_count(from_address)

        # Estimate gas if not provided
        if gas_limit is None:
            try:
                gas_limit = contract.functions.approve(
                    spender,
                    amount_wei
                ).estimate_gas({'from': from_address})
                gas_limit = int(gas_limit * 1.2)
            except Exception as e:
                raise RuntimeError(f"Gas estimation failed: {e}")

        # Get gas price
        if gas_price_gwei is not None:
            gas_price = self.w3.to_wei(gas_price_gwei, 'gwei')
        else:
            gas_price = self.w3.eth.gas_price

        # Build transaction
        transaction = contract.functions.approve(
            spender,
            amount_wei
        ).build_transaction({
            'from': from_address,
            'nonce': nonce,
            'gas': gas_limit,
            'gasPrice': gas_price,
        })

        # Sign and send
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        print(f"⏳ Approval sent: {tx_hash.hex()}")
        print(f"   Waiting for confirmation...")

        # Wait for receipt
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return self._format_receipt(receipt, 'approve')

    def transfer_from(
        self,
        token_address: str,
        private_key: str,
        from_address: str,
        to_address: str,
        amount: float,
        gas_limit: Optional[int] = None,
        gas_price_gwei: Optional[float] = None
    ) -> Dict:
        """
        Transfer tokens from another address (requires approval)

        Args:
            token_address: Token contract address
            private_key: Spender's private key
            from_address: Token owner address
            to_address: Recipient address
            amount: Amount to transfer
            gas_limit: Optional gas limit
            gas_price_gwei: Optional gas price in Gwei

        Returns:
            Transaction receipt
        """
        contract = self.get_contract(token_address)
        account = Account.from_key(private_key)
        spender = account.address

        # Get decimals and convert amount
        decimals = contract.functions.decimals().call()
        amount_wei = self._parse_amount(amount, decimals)

        # Check allowance
        allowance = contract.functions.allowance(from_address, spender).call()
        if allowance < amount_wei:
            raise ValueError(
                f"Insufficient allowance. Have: {self._format_amount(allowance, decimals)}, "
                f"Need: {amount}"
            )

        # Check owner balance
        balance = contract.functions.balanceOf(from_address).call()
        if balance < amount_wei:
            raise ValueError(
                f"Owner has insufficient balance. Have: {self._format_amount(balance, decimals)}, "
                f"Need: {amount}"
            )

        # Build transaction
        nonce = self.w3.eth.get_transaction_count(spender)

        # Estimate gas if not provided
        if gas_limit is None:
            try:
                gas_limit = contract.functions.transferFrom(
                    from_address,
                    to_address,
                    amount_wei
                ).estimate_gas({'from': spender})
                gas_limit = int(gas_limit * 1.2)
            except Exception as e:
                raise RuntimeError(f"Gas estimation failed: {e}")

        # Get gas price
        if gas_price_gwei is not None:
            gas_price = self.w3.to_wei(gas_price_gwei, 'gwei')
        else:
            gas_price = self.w3.eth.gas_price

        # Build transaction
        transaction = contract.functions.transferFrom(
            from_address,
            to_address,
            amount_wei
        ).build_transaction({
            'from': spender,
            'nonce': nonce,
            'gas': gas_limit,
            'gasPrice': gas_price,
        })

        # Sign and send
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        print(f"⏳ TransferFrom sent: {tx_hash.hex()}")
        print(f"   Waiting for confirmation...")

        # Wait for receipt
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return self._format_receipt(receipt, 'transferFrom')

    # ==================== Batch Operations ====================

    def transfer_batch(
        self,
        token_address: str,
        private_key: str,
        recipients: List[Tuple[str, float]],
        gas_price_gwei: Optional[float] = None
    ) -> List[Dict]:
        """
        Transfer tokens to multiple recipients

        Args:
            token_address: Token contract address
            private_key: Sender's private key
            recipients: List of (address, amount) tuples
            gas_price_gwei: Optional gas price in Gwei

        Returns:
            List of transaction receipts
        """
        account = Account.from_key(private_key)
        from_address = account.address

        # Get initial nonce
        nonce = self.w3.eth.get_transaction_count(from_address)

        receipts = []
        for i, (to_address, amount) in enumerate(recipients):
            print(f"\n📤 Transfer {i + 1}/{len(recipients)}: {amount} tokens to {to_address[:10]}...")

            try:
                receipt = self.transfer(
                    token_address=token_address,
                    private_key=private_key,
                    to_address=to_address,
                    amount=amount,
                    gas_price_gwei=gas_price_gwei
                )
                receipts.append(receipt)
                print(f"   ✅ Success!")

            except Exception as e:
                print(f"   ❌ Failed: {e}")
                receipts.append({
                    'success': False,
                    'error': str(e),
                    'to': to_address,
                    'amount': amount
                })

        return receipts

    # ==================== Event Listeners ====================

    def get_transfer_events(
        self,
        token_address: str,
        from_block: int = 0,
        to_block: int | str = 'latest',
        from_address: Optional[str] = None,
        to_address: Optional[str] = None
    ) -> List[Dict]:
        """
        Get Transfer events

        Args:
            token_address: Token contract address
            from_block: Starting block number
            to_block: Ending block number or 'latest'
            from_address: Filter by sender address
            to_address: Filter by recipient address

        Returns:
            List of Transfer events
        """
        contract = self.get_contract(token_address)
        decimals = contract.functions.decimals().call()

        # Build filter
        filter_params = {}
        if from_address:
            filter_params['from'] = from_address
        if to_address:
            filter_params['to'] = to_address

        # Get events
        events = contract.events.Transfer.get_logs(
            fromBlock=from_block,
            toBlock=to_block,
            argument_filters=filter_params
        )

        # Format events
        formatted_events = []
        for event in events:
            formatted_events.append({
                'block_number': event['blockNumber'],
                'transaction_hash': event['transactionHash'].hex(),
                'from': event['args']['from'],
                'to': event['args']['to'],
                'value': event['args']['value'],
                'value_formatted': self._format_amount(event['args']['value'], decimals),
            })

        return formatted_events

    # ==================== Utility Functions ====================

    def _parse_amount(self, amount: float, decimals: int) -> int:
        """Convert human-readable amount to wei"""
        return int(Decimal(str(amount)) * Decimal(10 ** decimals))

    def _format_amount(self, amount: int, decimals: int) -> float:
        """Convert wei to human-readable amount"""
        return float(Decimal(amount) / Decimal(10 ** decimals))

    def _format_receipt(self, receipt, tx_type: str) -> Dict:
        """Format transaction receipt"""
        success = receipt['status'] == 1

        return {
            'success': success,
            'type': tx_type,
            'hash': receipt['transactionHash'].hex(),
            'block_number': receipt['blockNumber'],
            'gas_used': receipt['gasUsed'],
            'effective_gas_price': receipt.get('effectiveGasPrice', 0),
            'transaction_index': receipt['transactionIndex'],
        }


def print_separator(title: str = ""):
    """พิมพ์เส้นแบ่ง"""
    if title:
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print('=' * 60)
    else:
        print('-' * 60)


def main():
    """ฟังก์ชันหลักสำหรับทดสอบ ERC-20 interaction"""

    print("🪙 ERC-20 Token Interaction Example")
    print("=" * 60)

    # NOTE: This example requires:
    # 1. A running Ethereum node (anvil, ganache, etc.)
    # 2. An ERC-20 token contract deployed
    # 3. Private keys for testing

    # Example token address (replace with your deployed token)
    # You can deploy the SimpleToken.sol contract first
    TOKEN_ADDRESS = os.getenv('TOKEN_ADDRESS', '0x5FbDB2315678afecb367f032d93F642f64180aa3')

    # Anvil default accounts for testing
    ACCOUNT_1_KEY = os.getenv('PRIVATE_KEY_1', '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80')
    ACCOUNT_2_KEY = os.getenv('PRIVATE_KEY_2', '0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d')

    ACCOUNT_1 = Account.from_key(ACCOUNT_1_KEY).address
    ACCOUNT_2 = Account.from_key(ACCOUNT_2_KEY).address

    try:
        # Initialize
        erc20 = ERC20Interact()

        # 1. Get token info
        print_separator("Token Information")
        info = erc20.get_token_info(TOKEN_ADDRESS)
        print(f"Name: {info['name']}")
        print(f"Symbol: {info['symbol']}")
        print(f"Decimals: {info['decimals']}")
        print(f"Total Supply: {info['total_supply_formatted']:,.2f} {info['symbol']}")
        print(f"Address: {info['address']}")

        # 2. Check balances
        print_separator("Account Balances")
        balance_1 = erc20.get_balance(TOKEN_ADDRESS, ACCOUNT_1)
        balance_2 = erc20.get_balance(TOKEN_ADDRESS, ACCOUNT_2)
        print(f"Account 1: {balance_1:,.2f} {info['symbol']}")
        print(f"  {ACCOUNT_1}")
        print(f"\nAccount 2: {balance_2:,.2f} {info['symbol']}")
        print(f"  {ACCOUNT_2}")

        # 3. Transfer tokens
        print_separator("Transfer Tokens")
        transfer_amount = 100.0
        print(f"Transferring {transfer_amount} {info['symbol']} from Account 1 to Account 2...")

        receipt = erc20.transfer(
            token_address=TOKEN_ADDRESS,
            private_key=ACCOUNT_1_KEY,
            to_address=ACCOUNT_2,
            amount=transfer_amount
        )

        if receipt['success']:
            print(f"✅ Transfer successful!")
            print(f"   Hash: {receipt['hash']}")
            print(f"   Gas used: {receipt['gas_used']:,}")
        else:
            print(f"❌ Transfer failed")

        # Check balances after transfer
        print("\nBalances after transfer:")
        balance_1_after = erc20.get_balance(TOKEN_ADDRESS, ACCOUNT_1)
        balance_2_after = erc20.get_balance(TOKEN_ADDRESS, ACCOUNT_2)
        print(f"Account 1: {balance_1_after:,.2f} {info['symbol']} (Δ {balance_1_after - balance_1:+,.2f})")
        print(f"Account 2: {balance_2_after:,.2f} {info['symbol']} (Δ {balance_2_after - balance_2:+,.2f})")

        # 4. Approve and TransferFrom
        print_separator("Approve & TransferFrom")
        approve_amount = 50.0
        print(f"Account 1 approving Account 2 to spend {approve_amount} {info['symbol']}...")

        receipt = erc20.approve(
            token_address=TOKEN_ADDRESS,
            private_key=ACCOUNT_1_KEY,
            spender=ACCOUNT_2,
            amount=approve_amount
        )

        if receipt['success']:
            print(f"✅ Approval successful!")
            print(f"   Hash: {receipt['hash']}")

            # Check allowance
            allowance = erc20.get_allowance(TOKEN_ADDRESS, ACCOUNT_1, ACCOUNT_2)
            print(f"\nAllowance: {allowance:,.2f} {info['symbol']}")

            # TransferFrom
            print(f"\nAccount 2 using transferFrom to move {approve_amount} from Account 1 to itself...")
            receipt = erc20.transfer_from(
                token_address=TOKEN_ADDRESS,
                private_key=ACCOUNT_2_KEY,
                from_address=ACCOUNT_1,
                to_address=ACCOUNT_2,
                amount=approve_amount
            )

            if receipt['success']:
                print(f"✅ TransferFrom successful!")
                print(f"   Hash: {receipt['hash']}")

                # Check final balances
                print("\nFinal balances:")
                balance_1_final = erc20.get_balance(TOKEN_ADDRESS, ACCOUNT_1)
                balance_2_final = erc20.get_balance(TOKEN_ADDRESS, ACCOUNT_2)
                print(f"Account 1: {balance_1_final:,.2f} {info['symbol']}")
                print(f"Account 2: {balance_2_final:,.2f} {info['symbol']}")

        # 5. Get Transfer events
        print_separator("Recent Transfer Events")
        events = erc20.get_transfer_events(
            token_address=TOKEN_ADDRESS,
            from_block=0,
            to_block='latest'
        )

        print(f"Found {len(events)} Transfer events:")
        for i, event in enumerate(events[-5:], 1):  # Show last 5
            print(f"\n{i}. Block {event['block_number']}")
            print(f"   From: {event['from']}")
            print(f"   To: {event['to']}")
            print(f"   Amount: {event['value_formatted']:,.2f} {info['symbol']}")
            print(f"   Tx: {event['transaction_hash'][:20]}...")

        print_separator()
        print("✅ All examples completed successfully!")

    except ConnectionError as e:
        print(f"\n❌ Connection Error: {e}")
        print("\n💡 Make sure you have a node running:")
        print("   anvil")
    except ValueError as e:
        print(f"\n❌ Value Error: {e}")
        print("\n💡 Make sure TOKEN_ADDRESS is set correctly in .env")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
