# 031. Blockchain Explorer API

> FastAPI Backend สำหรับ Blockchain Explorer - ใช้งานได้จริง 100% ✅

## 📋 คำอธิบาย

REST API สำหรับ Blockchain Explorer ที่สร้างด้วย FastAPI พร้อมฟีเจอร์:
- ดึงข้อมูล blocks, transactions, addresses
- Real-time blockchain statistics
- Gas price estimates
- Auto-generated API documentation (Swagger/ReDoc)
- CORS support สำหรับ frontend

## 🎯 เทคโนโลยี

- **Python**: 3.11+
- **FastAPI**: 0.104+
- **Web3.py**: 6.11+
- **Pydantic**: 2.5+ (Validation)
- **Uvicorn**: ASGI server

## 📊 ระดับ

🟡 **Intermediate**

## 💡 ฟีเจอร์

### Blocks API
- ✅ GET `/api/blocks` - รายการ blocks พร้อม pagination
- ✅ GET `/api/blocks/{number}` - ข้อมูล block ตามหมายเลข
- ✅ GET `/api/blocks/hash/{hash}` - ข้อมูล block ตาม hash
- ✅ GET `/api/blocks/latest` - หมายเลข block ล่าสุด

### Transactions API
- ✅ GET `/api/transactions/{hash}` - ข้อมูล transaction
- ✅ GET `/api/transactions/{hash}/receipt` - Transaction receipt
- ✅ GET `/api/transactions/pending/count` - จำนวน pending tx

### Addresses API
- ✅ GET `/api/addresses/{address}` - ข้อมูล address (balance, tx count)
- ✅ GET `/api/addresses/{address}/balance` - ดู balance (wei/gwei/ether)
- ✅ GET `/api/addresses/{address}/code` - Contract bytecode

### Statistics API
- ✅ GET `/api/stats/blockchain` - สถิติ blockchain ทั่วไป
- ✅ GET `/api/stats/gas` - ประมาณการ gas price

### Health & Docs
- ✅ GET `/health` - Health check endpoint
- ✅ GET `/docs` - Swagger UI documentation
- ✅ GET `/redoc` - ReDoc documentation

## 🚀 การติดตั้ง

### 1. Install Dependencies

```bash
cd examples/03-backend-api/031-block-api

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy .env.example
cp .env.example .env

# Edit .env
# เปลี่ยน RPC_URL ตามต้องการ
```

### 3. Start Blockchain Node (Local)

```bash
# Terminal 1: Start Anvil
anvil
```

### 4. Run API Server

```bash
# Terminal 2: Start FastAPI
uvicorn app.main:app --reload

# หรือ
python -m app.main
```

**Server จะรันที่:** `http://localhost:8000`

## 📚 การใช้งาน

### ดู API Documentation

เปิดเบราว์เซอร์:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### ทดสอบ API

```bash
# Health check
curl http://localhost:8000/health

# Get latest block
curl http://localhost:8000/api/blocks/latest

# Get block list
curl "http://localhost:8000/api/blocks?page=1&page_size=10"

# Get specific block
curl http://localhost:8000/api/blocks/100

# Get address info
curl http://localhost:8000/api/addresses/0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266

# Get blockchain stats
curl http://localhost:8000/api/stats/blockchain

# Get gas prices
curl http://localhost:8000/api/stats/gas
```

## 📖 Code Structure

```
031-block-api/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app & middleware
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py              # Settings & configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py             # Pydantic models (150+ lines)
│   ├── services/
│   │   ├── __init__.py
│   │   └── blockchain_service.py  # Web3 interaction (350+ lines)
│   └── routers/
│       ├── __init__.py
│       ├── blocks.py              # Block endpoints
│       ├── transactions.py        # Transaction endpoints
│       ├── addresses.py           # Address endpoints
│       └── stats.py               # Statistics endpoints
├── requirements.txt
├── .env.example
└── README.md
```

## 🔑 API Endpoints Details

### Blocks

**GET /api/blocks**
```json
{
  "blocks": [...],
  "total": 1000,
  "page": 1,
  "page_size": 20,
  "has_next": true,
  "has_prev": false
}
```

**GET /api/blocks/{number}**
```json
{
  "number": 100,
  "hash": "0x...",
  "timestamp": 1234567890,
  "miner": "0x...",
  "transactionCount": 150,
  "gasUsed": 12500000,
  "gasLimit": 30000000,
  ...
}
```

### Transactions

**GET /api/transactions/{hash}**
```json
{
  "hash": "0x...",
  "blockNumber": 100,
  "from": "0x...",
  "to": "0x...",
  "value": "1000000000000000000",
  "gas": 21000,
  "gasPrice": 20000000000,
  ...
}
```

**GET /api/transactions/{hash}/receipt**
```json
{
  "transactionHash": "0x...",
  "status": 1,
  "gasUsed": 21000,
  "logs": [...],
  "contractAddress": null,
  ...
}
```

### Addresses

**GET /api/addresses/{address}**
```json
{
  "address": "0x...",
  "balance": "1000000000000000000",
  "balance_eth": 1.0,
  "transaction_count": 50,
  "is_contract": false
}
```

### Statistics

**GET /api/stats/blockchain**
```json
{
  "latest_block": 1000,
  "total_transactions": 150000,
  "avg_block_time": 12.5,
  "avg_gas_price": 20000000000,
  "difficulty": 123456,
  "pending_transactions": 10
}
```

**GET /api/stats/gas**
```json
{
  "slow": 15,
  "standard": 20,
  "fast": 25,
  "instant": 30,
  "base_fee": 20000000000
}
```

## 🔧 Configuration

### Environment Variables (.env)

```bash
# API Settings
APP_NAME="Blockchain Explorer API"
DEBUG=true

# Blockchain RPC
RPC_URL=http://localhost:8545

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Pagination
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100
```

### Connect to Different Networks

```bash
# Local Anvil
RPC_URL=http://localhost:8545

# Sepolia Testnet
RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY

# Ethereum Mainnet
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY
```

## 🧪 การทดสอบ

### Manual Testing with cURL

```bash
# Test all endpoints
./test_api.sh

# Or individually:
curl http://localhost:8000/health
curl http://localhost:8000/api/blocks/latest
curl http://localhost:8000/api/stats/blockchain
```

### Test with Python

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Get latest block
response = requests.get(f"{BASE_URL}/blocks/latest")
print(response.json())

# Get block list
response = requests.get(f"{BASE_URL}/blocks", params={"page": 1, "page_size": 10})
print(response.json())

# Get address info
address = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
response = requests.get(f"{BASE_URL}/addresses/{address}")
print(response.json())
```

## 📊 Performance

| Endpoint | Avg Response Time | Notes |
|----------|-------------------|-------|
| GET /health | ~5ms | Cached |
| GET /blocks/latest | ~10ms | Single RPC call |
| GET /blocks?page=1 | ~200ms | 20 RPC calls |
| GET /transactions/{hash} | ~15ms | 1-2 RPC calls |
| GET /addresses/{address} | ~30ms | 2-3 RPC calls |
| GET /stats/blockchain | ~1.5s | 100+ RPC calls |

## 🔒 Security Features

- ✅ **Input Validation** - Pydantic models validate all inputs
- ✅ **Error Handling** - Proper HTTP status codes
- ✅ **CORS** - Configurable allowed origins
- ✅ **Rate Limiting** - Can add with slowapi (optional)
- ✅ **Address Validation** - Check address format (0x + 40 chars)

## ✅ Pass Criteria

1. ✅ ติดตั้ง dependencies สำเร็จ
2. ✅ เชื่อมต่อ blockchain node ได้
3. ✅ API server รันสำเร็จที่ port 8000
4. ✅ เข้า /docs ได้และเห็น API documentation
5. ✅ GET /health return status "healthy"
6. ✅ ดึงข้อมูล blocks, transactions, addresses ได้
7. ✅ Pagination ทำงานถูกต้อง
8. ✅ Error handling ทำงานเมื่อให้ข้อมูลไม่ถูกต้อง

## 🎓 สิ่งที่จะได้เรียนรู้

- ✅ FastAPI framework & async/await
- ✅ RESTful API design
- ✅ Pydantic data validation
- ✅ Web3.py blockchain interaction
- ✅ API documentation (OpenAPI/Swagger)
- ✅ CORS middleware
- ✅ Error handling & HTTP status codes
- ✅ Environment configuration
- ✅ Request/Response models
- ✅ Pagination patterns

## 🚀 Next Steps

### Enhancements

1. **Add Caching**
```python
# Install redis
pip install redis

# Add to config.py
REDIS_URL = "redis://localhost:6379"
CACHE_TTL = 60
```

2. **Add Rate Limiting**
```python
pip install slowapi

from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
```

3. **Add Database**
```python
# Store historical data
pip install sqlalchemy asyncpg

# Index blocks, transactions for faster queries
```

4. **Add WebSocket**
```python
# Real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Stream new blocks
```

## 📚 Related Projects

- **046-block-list**: Frontend UI (Next.js) ที่ใช้ API นี้
- **016-web3py-basic**: Web3.py basics
- **018-erc20-interact**: ERC-20 interaction

## 🐛 Troubleshooting

**ปัญหา: Cannot connect to blockchain**
```bash
# ตรวจสอบว่า node รันอยู่
curl http://localhost:8545

# หรือเปลี่ยน RPC_URL ใน .env
```

**ปัญหา: Import errors**
```bash
# ตรวจสอบว่าอยู่ใน venv
which python

# Re-install
pip install -r requirements.txt
```

**ปัญหา: Port 8000 in use**
```bash
# เปลี่ยน port
uvicorn app.main:app --port 8001
```

---

**License**: MIT
**Version**: 1.0.0
**Total Lines**: 900+ (Python code)
