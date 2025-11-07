# 016. Web3.py Basic Connection

> เชื่อมต่อกับ Ethereum node และดึงข้อมูลพื้นฐาน - ใช้งานได้จริง 100% ✅

## 📋 คำอธิบาย

เรียนรู้การใช้ Web3.py เพื่อเชื่อมต่อกับ Ethereum node และดึงข้อมูลพื้นฐาน เช่น blocks, transactions, balances

## 🎯 เทคโนโลยี

- **Python**: 3.11+
- **Web3.py**: 6.11+
- **python-dotenv**: สำหรับ environment variables

## 📊 ระดับ

🟢 **Beginner**

## 💡 ฟีเจอร์

- ✅ **Connection Management** - เชื่อมต่อกับ Ethereum node (HTTP/WebSocket/IPC)
- ✅ **Block Information** - ดึงข้อมูล blocks และ latest block number
- ✅ **Transaction Data** - ดูรายละเอียด transactions
- ✅ **Balance Checking** - ตรวจสอบ ETH balance ของ address
- ✅ **Gas Price** - ดู gas price ปัจจุบัน
- ✅ **Wei Conversion** - แปลงระหว่าง ETH, Gwei, Wei
- ✅ **Address Validation** - ตรวจสอบ address และ checksum

## 🚀 การติดตั้ง

### 1. Install Dependencies

```bash
# สร้าง virtual environment (แนะนำ)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# หรือ venv\Scripts\activate  # Windows

# ติดตั้ง packages
pip install -r requirements.txt
```

### 2. Setup Environment

```bash
# Copy environment file
cp .env.example .env

# แก้ไข .env (optional)
# RPC_URL=http://localhost:8545
```

### 3. Start Local Node (Optional)

```bash
# Option 1: Anvil (Foundry)
anvil

# Option 2: Ganache
ganache-cli
```

## 📚 การใช้งาน

### รันโปรแกรม

```bash
python main.py
```

**Expected Output:**
```
🔗 Web3.py Basic Connection Example
============================================================

📡 Connecting to: http://localhost:8545
✅ Connected successfully!

============================================================
  Network Information
============================================================
Chain ID: 31337
Latest Block: 0
Gas Price: 1.00 Gwei

============================================================
  Latest Block Details
============================================================
Block Number: 0
Block Hash: 0x...
Timestamp: 1699999999
Miner: 0x...
Gas Used: 0 / 30,000,000
Transactions: 0

============================================================
  Account Information
============================================================

Account #1:
  Address: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
  Balance: 10000.0000 ETH
  Transactions: 0

...
```

### ใช้ใน Python Code

```python
from main import Web3Connection

# สร้าง connection
web3 = Web3Connection()

# ตรวจสอบการเชื่อมต่อ
if web3.is_connected():
    print("Connected!")

# ดึงข้อมูล block
block = web3.get_block('latest')
print(f"Latest block: {block['number']}")

# ดู balance
balance = web3.get_balance("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")
print(f"Balance: {balance} ETH")

# แปลง Wei
wei_amount = web3.to_wei(1.5, 'ether')
eth_amount = web3.from_wei(wei_amount, 'ether')
```

## 📖 Code Structure

```
016-web3py-basic/
├── main.py              # 258 lines - Complete implementation
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
└── README.md            # This file
```

## 🔧 API Reference

### Web3Connection Class

```python
class Web3Connection:
    def __init__(self, rpc_url: Optional[str] = None)
    def is_connected() -> bool
    def get_chain_id() -> int
    def get_latest_block_number() -> int
    def get_block(block_identifier) -> dict
    def get_transaction(tx_hash: str) -> dict
    def get_balance(address: str) -> float
    def get_transaction_count(address: str) -> int
    def get_gas_price() -> float
    def to_wei(amount: float, unit: str = 'ether') -> int
    def from_wei(amount: int, unit: str = 'ether') -> float
    def is_address(address: str) -> bool
    def to_checksum_address(address: str) -> str
```

## 💡 ตัวอย่างการใช้งาน

### 1. เชื่อมต่อกับ network ต่างๆ

```python
# Localhost
web3_local = Web3Connection("http://localhost:8545")

# Mainnet (Alchemy)
web3_mainnet = Web3Connection("https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY")

# Sepolia Testnet
web3_sepolia = Web3Connection("https://eth-sepolia.g.alchemy.com/v2/YOUR_KEY")
```

### 2. ดึงข้อมูล Block

```python
# Latest block
latest = web3.get_block('latest')
print(f"Block {latest['number']} has {latest['transaction_count']} txs")

# Specific block number
block_100 = web3.get_block(100)
print(f"Block hash: {block_100['hash']}")
```

### 3. ตรวจสอบ Balance

```python
address = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
balance = web3.get_balance(address)
print(f"{address} has {balance:.4f} ETH")

# Transaction count (nonce)
nonce = web3.get_transaction_count(address)
print(f"Total transactions: {nonce}")
```

### 4. Wei Conversions

```python
# ETH to Wei
eth_amount = 1.5
wei_amount = web3.to_wei(eth_amount, 'ether')
# 1500000000000000000

# Gwei to Wei
gwei_amount = 50
wei_from_gwei = web3.to_wei(gwei_amount, 'gwei')
# 50000000000

# Wei to ETH
back_to_eth = web3.from_wei(wei_amount, 'ether')
# 1.5
```

### 5. Address Validation

```python
address = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"

# Validate
is_valid = web3.is_address(address)  # True

# Convert to checksum
checksum = web3.to_checksum_address(address.lower())
# 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
```

## ✅ Pass Criteria

1. ✅ ติดตั้ง dependencies สำเร็จ (web3, python-dotenv)
2. ✅ เชื่อมต่อกับ Ethereum node สำเร็จ
3. ✅ ดึงข้อมูล latest block ได้
4. ✅ ตรวจสอบ balance ได้
5. ✅ แปลง Wei conversion ถูกต้อง
6. ✅ Address validation ทำงานถูกต้อง

## 🐛 Troubleshooting

### ❌ "Failed to connect to Ethereum node"

**สาเหตุ**: ไม่มี node running

**แก้ไข**:
```bash
# Start Anvil
anvil

# หรือ Ganache
ganache-cli

# หรือตั้ง RPC_URL ใน .env ไปยัง remote node
RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY
```

### ❌ "ModuleNotFoundError: No module named 'web3'"

**แก้ไข**:
```bash
pip install web3
```

## 🎓 สิ่งที่จะได้เรียนรู้

- ✅ การเชื่อมต่อกับ Ethereum node ด้วย Web3.py
- ✅ การดึงข้อมูล blocks และ transactions
- ✅ การตรวจสอบ balance และ nonce
- ✅ การแปลงระหว่าง ETH, Gwei, Wei
- ✅ Address validation และ checksum
- ✅ การใช้ environment variables
- ✅ Error handling และ connection management

## 🚀 Next Steps

หลังจากเรียนรู้โปรเจคนี้แล้ว ลองดู:

- **017-send-eth**: ส่ง ETH transactions
- **018-erc20-interact**: โต้ตอบกับ ERC-20 tokens
- **020-event-listener**: ฟัง blockchain events

## 📚 เอกสารเพิ่มเติม

- [Web3.py Documentation](https://web3py.readthedocs.io/)
- [Ethereum JSON-RPC API](https://ethereum.org/en/developers/docs/apis/json-rpc/)

---

**License**: MIT
**Author**: Blockchain Explorer Examples
**Version**: 1.0.0
