# 018. ERC-20 Token Interaction

> โต้ตอบกับ ERC-20 tokens ด้วย Web3.py - Transfer, Approve, Balance - ใช้งานได้จริง 100% ✅

## 📋 คำอธิบาย

เรียนรู้การโต้ตอบกับ ERC-20 tokens ด้วย Web3.py พร้อม:
- Get token metadata
- Check balance
- Transfer tokens
- Approve & TransferFrom
- Batch transfers
- Listen to events

## 🎯 เทคโนโลยี

- **Python**: 3.11+
- **Web3.py**: 6.11+
- **eth-account**: 0.10+

## 📊 ระดับ

🟢 **Beginner**

## 💡 ฟีเจอร์

- ✅ **Get Token Info** - ดึงข้อมูล name, symbol, decimals, totalSupply
- ✅ **Balance Check** - ตรวจสอบ balance ของ address
- ✅ **Transfer** - ส่ง tokens พร้อม gas estimation
- ✅ **Approve** - อนุมัติให้ address อื่นใช้ tokens
- ✅ **TransferFrom** - ส่ง tokens จาก address ที่ได้รับอนุมัติ
- ✅ **Batch Transfer** - ส่งไปหลาย addresses พร้อมกัน
- ✅ **Event Listener** - ฟัง Transfer events
- ✅ **Allowance Check** - ตรวจสอบจำนวนที่อนุมัติ

## 🚀 การติดตั้ง

```bash
# Install dependencies
pip install -r requirements.txt

# Start Anvil
anvil

# Deploy ERC-20 token (ใช้โปรเจค 001-basic-erc20)
# หรือใช้ token ที่มีอยู่แล้ว
```

## 📚 การใช้งาน

### รันโปรแกรม

```bash
python erc20_interact.py
```

### ใช้ใน Code

```python
from erc20_interact import ERC20Interact

# Initialize
erc20 = ERC20Interact()

# Get token info
info = erc20.get_token_info("0x5FbDB231...")
print(f"{info['name']} ({info['symbol']})")
print(f"Decimals: {info['decimals']}")
print(f"Total Supply: {info['total_supply_formatted']}")

# Check balance
balance = erc20.get_balance(
    token_address="0x5FbDB231...",
    account_address="0xf39Fd6e51..."
)
print(f"Balance: {balance} tokens")
```

### Transfer Tokens

```python
# Transfer tokens
receipt = erc20.transfer(
    token_address="0x5FbDB231...",
    private_key="0xac0974...",
    to_address="0x70997970...",
    amount=100.0  # 100 tokens
)

print(f"Hash: {receipt['hash']}")
print(f"Gas used: {receipt['gas_used']}")
```

### Approve & TransferFrom

```python
# Approve spender
receipt = erc20.approve(
    token_address="0x5FbDB231...",
    private_key="0xac0974...",
    spender="0x70997970...",
    amount=50.0
)

# Check allowance
allowance = erc20.get_allowance(
    token_address="0x5FbDB231...",
    owner="0xf39Fd6e51...",
    spender="0x70997970..."
)

# TransferFrom
receipt = erc20.transfer_from(
    token_address="0x5FbDB231...",
    private_key="0x59c6995e...",  # Spender's key
    from_address="0xf39Fd6e51...",  # Owner
    to_address="0x3C44CdDdB...",  # Recipient
    amount=50.0
)
```

### Batch Transfer

```python
recipients = [
    ("0x70997970C51812dc3A010C7d01b50e0d17dc79C8", 10.0),
    ("0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC", 20.0),
    ("0x90F79bf6EB2c4f870365E785982E1f101E93b906", 30.0),
]

receipts = erc20.transfer_batch(
    token_address="0x5FbDB231...",
    private_key="0xac0974...",
    recipients=recipients
)
```

### Listen to Events

```python
# Get all Transfer events
events = erc20.get_transfer_events(
    token_address="0x5FbDB231...",
    from_block=0,
    to_block='latest'
)

for event in events:
    print(f"From: {event['from']}")
    print(f"To: {event['to']}")
    print(f"Amount: {event['value_formatted']}")

# Filter by sender
events = erc20.get_transfer_events(
    token_address="0x5FbDB231...",
    from_address="0xf39Fd6e51..."
)
```

## 📖 Code Structure

```
018-erc20-interact/
├── erc20_interact.py   # 784 lines - Complete implementation
├── requirements.txt    # Dependencies
├── .env.example        # Environment template
└── README.md           # This file
```

## 🔑 Key Methods

### ERC20Interact Class

**Read Functions:**
- `get_token_info(token_address)` - Get metadata
- `get_balance(token_address, account)` - Get balance
- `get_allowance(token_address, owner, spender)` - Get allowance

**Write Functions:**
- `transfer(token_address, private_key, to, amount)` - Transfer tokens
- `approve(token_address, private_key, spender, amount)` - Approve spending
- `transfer_from(token_address, private_key, from, to, amount)` - Transfer from approved

**Batch Operations:**
- `transfer_batch(token_address, private_key, recipients)` - Batch transfer

**Events:**
- `get_transfer_events(token_address, from_block, to_block)` - Get Transfer events

## ✅ Pass Criteria

1. ✅ เชื่อมต่อกับ node สำเร็จ
2. ✅ ดึงข้อมูล token metadata ได้
3. ✅ ตรวจสอบ balance ได้
4. ✅ Transfer tokens สำเร็จ
5. ✅ Approve และ TransferFrom ทำงานถูกต้อง
6. ✅ ฟัง events ได้

## 🎓 สิ่งที่จะได้เรียนรู้

- ✅ ERC-20 standard functions
- ✅ การโต้ตอบกับ smart contracts
- ✅ Contract ABI และการใช้งาน
- ✅ Token decimals และการแปลงค่า
- ✅ Approve/TransferFrom pattern
- ✅ Gas estimation สำหรับ contract calls
- ✅ Event filtering และ parsing
- ✅ Batch transaction sending

## 🔧 Environment Variables

สร้างไฟล์ `.env`:

```bash
# RPC endpoint
RPC_URL=http://localhost:8545

# Token contract address
TOKEN_ADDRESS=0x5FbDB2315678afecb367f032d93F642f64180aa3

# Test accounts (Anvil defaults)
PRIVATE_KEY_1=0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
PRIVATE_KEY_2=0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d
```

## 💡 Example Output

```
🪙 ERC-20 Token Interaction Example
============================================================

============================================================
  Token Information
============================================================
Name: MyToken
Symbol: MTK
Decimals: 18
Total Supply: 1,000,000.00 MTK
Address: 0x5FbDB2315678afecb367f032d93F642f64180aa3

============================================================
  Account Balances
============================================================
Account 1: 1,000,000.00 MTK
  0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266

Account 2: 0.00 MTK
  0x70997970C51812dc3A010C7d01b50e0d17dc79C8

============================================================
  Transfer Tokens
============================================================
Transferring 100.0 MTK from Account 1 to Account 2...
⏳ Transaction sent: 0xabc123...
   Waiting for confirmation...
✅ Transfer successful!
   Hash: 0xabc123...
   Gas used: 51,623

Balances after transfer:
Account 1: 999,900.00 MTK (Δ -100.00)
Account 2: 100.00 MTK (Δ +100.00)
```

## 🚀 Next Steps

- **019-contract-deploy**: Deploy contracts ด้วย Web3.py
- **020-event-listener**: Event listener ขั้นสูง
- **022-web3js-basic**: Web3.js (JavaScript version)

## 📚 Related Projects

- **001-basic-erc20**: ERC-20 Token contract (Solidity)
- **016-web3py-basic**: Web3.py connection basics
- **017-send-eth**: Send ETH transactions

---

**License**: MIT
**Version**: 1.0.0
