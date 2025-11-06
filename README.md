# 🔗 Blockchain Explorer System - คู่มือการใช้งานโปรเจกต์

> ระบบ Block Explorer แบบครบวงจร คล้าย Etherscan พร้อมใช้งานจริง 100%

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Compatible-326CE5.svg)](https://kubernetes.io/)

---

## 📋 สารบัญ

- [ภาพรวมโปรเจกต์](#ภาพรวมโปรเจกต์)
- [คุณสมบัติหลัก](#คุณสมบัติหลัก)
- [สถาปัตยกรรมระบบ](#สถาปัตยกรรมระบบ)
- [เทคโนโลยีที่ใช้](#เทคโนโลยีที่ใช้)
- [การติดตั้งและเริ่มต้นใช้งาน](#การติดตั้งและเริ่มต้นใช้งาน)
- [โครงสร้างโปรเจกต์](#โครงสร้างโปรเจกต์)
- [การใช้งาน](#การใช้งาน)
- [เอกสารประกอบ](#เอกสารประกอบ)
- [การพัฒนา](#การพัฒนา)
- [การทดสอบ](#การทดสอบ)
- [การ Deploy](#การ-deploy)
- [FAQ](#faq)
- [การสนับสนุน](#การสนับสนุน)

---

## 🎯 ภาพรวมโปรเจกต์

**Blockchain Explorer System** เป็นระบบสำรวจบลอกเชนแบบครบวงจรที่ออกแบบมาเพื่อให้ผู้ใช้สามารถค้นหา วิเคราะห์ และติดตามข้อมูลบน blockchain ได้อย่างมีประสิทธิภาพ คล้ายกับ Etherscan แต่สามารถ self-host และปรับแต่งได้เต็มที่

### 🎯 เป้าหมายของโปรเจกต์

1. **ความโปร่งใส**: ให้ผู้ใช้เข้าถึงข้อมูล blockchain ได้ง่ายและชัดเจน
2. **ประสิทธิภาพ**: รองรับการค้นหาและวิเคราะห์ข้อมูลขนาดใหญ่ได้รวดเร็ว
3. **ความยืดหยุ่น**: สามารถปรับแต่งและขยายระบบได้ตามความต้องการ
4. **ความน่าเชื่อถือ**: ระบบมีความเสถียรและพร้อมใช้งานแบบ production-ready

---

## ✨ คุณสมบัติหลัก

### 🔍 การค้นหาและสำรวจ

- ✅ **ค้นหาธุรกรรม (Transaction)**: ค้นหาด้วย transaction hash
- ✅ **ค้นหาบลอก (Block)**: ดูข้อมูลบลอกตามหมายเลขหรือ hash
- ✅ **ค้นหาที่อยู่ (Address)**: ดูประวัติธุรกรรมและยอดคงเหลือ
- ✅ **ค้นหา Token**: ดูข้อมูล ERC-20, ERC-721, ERC-1155
- ✅ **Smart Search**: ระบบค้นหาอัจฉริยะที่รองรับหลายรูปแบบ

### 📊 การวิเคราะห์ข้อมูล

- 📈 **Network Statistics**: สถิติเครือข่ายแบบเรียลไทม์
- 📉 **Gas Analytics**: วิเคราะห์ค่าธรรมเนียม gas และแนวโน้ม
- 🔝 **Top Addresses**: รายการที่อยู่ยอดนิยมตาม volume และจำนวนธุรกรรม
- 💰 **Token Analytics**: วิเคราะห์การเคลื่อนไหวของ token
- 📊 **Daily Aggregations**: สถิติรวมรายวัน/รายชั่วโมง

### 🛠️ คุณสมบัติขั้นสูง

- 🔄 **Real-time Updates**: อัปเดตข้อมูลแบบเรียลไทม์
- 🗂️ **Internal Transactions**: ติดตาม internal transactions
- 📝 **Event Logs Decoding**: ถอดรหัส event logs ด้วย ABI
- 🏷️ **Address Labels**: ติดป้ายกำกับที่อยู่ (contracts, routers, etc.)
- 📤 **Data Export**: ส่งออกข้อมูลเป็น CSV/Parquet
- 🔐 **Contract Verification**: ตรวจสอบ source code ของ smart contracts (roadmap)

### 🖥️ User Interface

- 🌓 **Dark/Light Mode**: รองรับทั้งโหมดมืดและสว่าง
- 📱 **Responsive Design**: ใช้งานได้ทุกอุปกรณ์
- ♿ **Accessibility**: ออกแบบให้เข้าถึงได้สำหรับทุกคน
- 🚀 **Fast Loading**: SSR/ISR เพื่อความเร็วในการโหลด

---

## 🏗️ สถาปัตยกรรมระบบ

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Blockchain Explorer                          │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────┐      RPC/WS     ┌──────────────────────┐
│     Ethereum Node (Geth)     │◄────────────────│  Indexer (ETL Jobs)  │
│   - Mainnet / Sepolia        │                 │  - Python (web3.py)  │
│   - Archive Mode             │                 │  - TypeScript         │
└──────────────┬───────────────┘                 └─────────────┬────────┘
               │                                                │
               │ blocks/transactions/logs                       │ upsert
               │                                                │
               ▼                                                ▼
        ┌──────────────┐                              ┌─────────────────┐
        │   Anvil       │                              │   PostgreSQL    │
        │ (Local Dev)   │                              │   - Blocks      │
        └───────────────┘                              │   - Transactions│
                                                       │   - Logs        │
                                                       │   - Addresses   │
                                                       │   - Tokens      │
                                                       └────────┬────────┘
                                                                │
                                                                │ analytics
                                                                ▼
                                                       ┌─────────────────┐
        ┌──────────────┐    ◄───── Cache ─────►       │  ClickHouse     │
        │    Redis     │                               │  - Fact Tables  │
        │  - Cache     │                               │  - Aggregations │
        │  - Sessions  │                               └────────┬────────┘
        └──────┬───────┘                                        │
               │                                                 │
               │                                                 │
               ▼                                                 ▼
        ┌──────────────────┐                           ┌─────────────────┐
        │   FastAPI/REST   │◄──────────────────────────│   Next.js UI    │
        │   - /blocks      │        HTTP/GraphQL       │   - Home        │
        │   - /txs         │                           │   - Block View  │
        │   - /address     │                           │   - Tx View     │
        │   - /tokens      │                           │   - Address     │
        │   - /search      │                           │   - Token View  │
        └──────┬───────────┘                           │   - Search      │
               │                                       └─────────────────┘
               │ metrics/logs
               ▼
        ┌────────────────────┐
        │ Prometheus/Grafana │
        │  - Metrics         │
        │  - Dashboards      │
        │  - Alerts          │
        └────────────────────┘

Optional: Message Queue Layer
┌──────────────────────────────┐
│  Kafka / Redpanda            │
│  - Block Events              │
│  - Transaction Events        │
│  - Log Events                │
└──────────────────────────────┘
```

### 🔄 Data Flow

1. **Block Ingestion**: Indexer ดึงข้อมูลจาก Ethereum node ผ่าน RPC
2. **Data Processing**: แปลงและทำ normalize ข้อมูล
3. **Storage**: เก็บลงใน PostgreSQL (OLTP) และ ClickHouse (Analytics)
4. **API Layer**: FastAPI เสิร์ฟข้อมูลผ่าน REST/GraphQL API
5. **Caching**: Redis cache ข้อมูลที่เข้าถึงบ่อย
6. **Frontend**: Next.js ดึงข้อมูลจาก API และแสดงผล
7. **Monitoring**: Prometheus/Grafana เก็บ metrics และสร้าง dashboard

---

## 🛠️ เทคโนโลยีที่ใช้

### Blockchain Layer
- **[Geth](https://geth.ethereum.org/)** - Ethereum client (production)
- **[Anvil](https://book.getfoundry.sh/anvil/)** - Local development node
- **[Web3.py](https://web3py.readthedocs.io/)** - Python Ethereum library
- **[Ethers.js](https://docs.ethers.org/)** - TypeScript Ethereum library

### Smart Contracts
- **[Solidity](https://soliditylang.org/)** - Smart contract language
- **[Foundry](https://book.getfoundry.sh/)** - Development framework
- **[Hardhat](https://hardhat.org/)** - Alternative framework (optional)

### Database Layer
- **[PostgreSQL 15+](https://www.postgresql.org/)** - OLTP database
- **[ClickHouse](https://clickhouse.com/)** - Analytics database
- **[Redis](https://redis.io/)** - Caching and session storage

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Python API framework
- **[Python 3.11+](https://www.python.org/)** - Backend language
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - ORM
- **[Alembic](https://alembic.sqlalchemy.org/)** - Database migrations

### Frontend
- **[Next.js 14](https://nextjs.org/)** - React framework with SSR/ISR
- **[React 18](https://react.dev/)** - UI library
- **[TypeScript](https://www.typescriptlang.org/)** - Type-safe JavaScript
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first CSS
- **[shadcn/ui](https://ui.shadcn.com/)** - Component library

### Observability
- **[Prometheus](https://prometheus.io/)** - Metrics collection
- **[Grafana](https://grafana.com/)** - Metrics visualization
- **[Loki](https://grafana.com/oss/loki/)** - Log aggregation (optional)

### Message Queue (Optional)
- **[Kafka](https://kafka.apache.org/)** - Distributed streaming
- **[Redpanda](https://redpanda.com/)** - Kafka alternative

### DevOps
- **[Docker](https://www.docker.com/)** - Containerization
- **[Docker Compose](https://docs.docker.com/compose/)** - Multi-container orchestration
- **[Kubernetes](https://kubernetes.io/)** - Container orchestration (optional)
- **[Helm](https://helm.sh/)** - Kubernetes package manager (optional)

---

## 🚀 การติดตั้งและเริ่มต้นใช้งาน

### ความต้องการของระบบ

#### Hardware Requirements
- **CPU**: 4+ cores (8+ cores แนะนำ)
- **RAM**: 16GB minimum (32GB+ แนะนำ)
- **Storage**: 500GB+ SSD (สำหรับ archive node)
- **Network**: High-bandwidth internet connection

#### Software Requirements
- **Docker**: 24.0.0+
- **Docker Compose**: 2.20.0+
- **Node.js**: 20.0.0+ (สำหรับ frontend development)
- **Python**: 3.11+ (สำหรับ backend development)
- **Git**: 2.40.0+

### Quick Start (Docker Compose)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/blockchain-explorer.git
cd blockchain-explorer

# 2. Copy environment file
cp .env.example .env

# 3. แก้ไขไฟล์ .env ตามความต้องการ
nano .env

# 4. Start all services
docker-compose up -d

# 5. ตรวจสอบสถานะ
docker-compose ps

# 6. ดู logs
docker-compose logs -f indexer
```

### การเข้าถึง Services

หลังจาก start services แล้ว สามารถเข้าถึงได้ที่:

| Service | URL | Description |
|---------|-----|-------------|
| **Explorer UI** | http://localhost:3000 | หน้าเว็บ Block Explorer |
| **API Docs** | http://localhost:8000/docs | FastAPI Swagger UI |
| **Grafana** | http://localhost:3001 | Metrics Dashboard (admin/admin) |
| **Prometheus** | http://localhost:9090 | Metrics Database |
| **PostgreSQL** | localhost:5432 | Database (postgres/postgres) |
| **Redis** | localhost:6379 | Cache Server |

### Development Setup

#### Backend (FastAPI)

```bash
cd services/api

# สร้าง virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# หรือ
.\venv\Scripts\activate  # Windows

# ติดตั้ง dependencies
pip install -r requirements.txt

# รัน migrations
alembic upgrade head

# Start development server
uvicorn fastapi_app.main:app --reload --port 8000
```

#### Frontend (Next.js)

```bash
cd services/ui/nextjs

# ติดตั้ง dependencies
npm install

# Start development server
npm run dev
```

#### Indexer (Python)

```bash
cd services/indexer/py

# สร้าง virtual environment
python -m venv venv
source venv/bin/activate

# ติดตั้ง dependencies
pip install -r requirements.txt

# รัน indexer
python main.py
```

---

## 📁 โครงสร้างโปรเจกต์

```
blockchain-explorer/
├── 📄 README.md                      # เอกสารหลัก (ไฟล์นี้)
├── 📄 TUTORIAL.md                    # คู่มือการสอนแบบละเอียด
├── 📄 SUMMARY.md                     # สรุปภาพรวมโปรเจกต์
├── 📄 TASK.md                        # รายการงานที่ต้องทำ
├── 📄 CHECKLIST.md                   # รายการตรวจสอบ
├── 📄 TODO.md                        # Todo list
├── 📄 docker-compose.yml             # Docker orchestration
├── 📄 .env.example                   # ตัวอย่าง environment variables
│
├── 📂 docs/                          # เอกสารประกอบ
│   └── 📂 parts/                     # เอกสารแบ่งเป็นส่วน
│       ├── PART01.md                 # พื้นฐานและการติดตั้ง
│       ├── PART02.md                 # Blockchain Nodes
│       ├── PART03.md                 # Smart Contracts
│       ├── PART04.md                 # Database Design
│       ├── PART05.md                 # Indexer & ETL
│       ├── PART06.md                 # API Layer
│       ├── PART07.md                 # Explorer UI
│       ├── PART08.md                 # Analytics
│       ├── PART09.md                 # Monitoring
│       ├── PART10.md                 # Security
│       ├── PART11.md                 # Deployment
│       └── PART12.md                 # Testing
│
├── 📂 services/                      # Services directory
│   ├── 📂 geth/                      # Geth node config
│   │   ├── entrypoint.sh
│   │   └── genesis.json
│   │
│   ├── 📂 anvil/                     # Anvil local node
│   │   └── start.sh
│   │
│   ├── 📂 indexer/                   # Indexer services
│   │   ├── 📂 py/                    # Python indexer
│   │   │   ├── main.py
│   │   │   ├── requirements.txt
│   │   │   ├── config.py
│   │   │   ├── indexer.py
│   │   │   └── models.py
│   │   │
│   │   └── 📂 ts/                    # TypeScript indexer
│   │       ├── package.json
│   │       ├── tsconfig.json
│   │       └── src/
│   │
│   ├── 📂 api/                       # Backend API
│   │   └── 📂 fastapi_app/
│   │       ├── main.py
│   │       ├── requirements.txt
│   │       ├── 📂 routers/
│   │       ├── 📂 models/
│   │       ├── 📂 schemas/
│   │       ├── 📂 services/
│   │       └── 📂 tests/
│   │
│   ├── 📂 ui/                        # Frontend
│   │   └── 📂 nextjs/
│   │       ├── package.json
│   │       ├── next.config.js
│   │       ├── 📂 app/
│   │       ├── 📂 components/
│   │       ├── 📂 lib/
│   │       └── 📂 public/
│   │
│   └── 📂 observability/             # Monitoring
│       ├── 📂 prometheus/
│       │   └── prometheus.yml
│       └── 📂 grafana/
│           ├── datasources.yml
│           └── dashboards/
│
├── 📂 db/                            # Database schemas
│   ├── 📂 postgres/
│   │   ├── init.sql
│   │   ├── schema.sql
│   │   └── indexes.sql
│   │
│   └── 📂 clickhouse/
│       ├── init.sql
│       └── schema.sql
│
├── 📂 contracts/                     # Smart contracts
│   ├── 📂 src/
│   │   ├── Token.sol
│   │   └── NFT.sol
│   ├── 📂 test/
│   ├── 📂 script/
│   └── foundry.toml
│
├── 📂 tests/                         # Tests
│   ├── 📂 e2e/                       # End-to-end tests
│   ├── 📂 data-quality/              # Data quality tests
│   └── 📂 retrieval-metrics/         # Search quality tests
│
└── 📂 k8s/                           # Kubernetes configs (optional)
    ├── 📂 base/
    ├── 📂 overlays/
    └── 📂 helm/
```

---

## 💻 การใช้งาน

### 1. การค้นหาข้อมูล

#### ค้นหา Transaction

```bash
# ใช้ Web UI
เปิด http://localhost:3000 และใส่ transaction hash ในช่องค้นหา

# ใช้ API
curl http://localhost:8000/api/v1/txs/0x1234...
```

#### ค้นหา Block

```bash
# By block number
curl http://localhost:8000/api/v1/blocks/12345

# By block hash
curl http://localhost:8000/api/v1/blocks/0xabc...
```

#### ค้นหา Address

```bash
curl http://localhost:8000/api/v1/address/0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
```

### 2. การใช้งาน API

#### Authentication (ถ้ามี)

```bash
# Get API key
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"secret"}'

# Use API key
curl http://localhost:8000/api/v1/blocks/latest \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### Pagination

```bash
# Get transactions with pagination
curl "http://localhost:8000/api/v1/txs?page=1&limit=20"
```

#### Filtering

```bash
# Get transactions by address
curl "http://localhost:8000/api/v1/txs?address=0x123...&sort=desc"
```

### 3. การส่งออกข้อมูล

```bash
# Export to CSV
curl "http://localhost:8000/api/v1/export/txs?format=csv&from_block=1&to_block=1000" \
  -o transactions.csv

# Export to Parquet
curl "http://localhost:8000/api/v1/export/txs?format=parquet&from_block=1&to_block=1000" \
  -o transactions.parquet
```

---

## 📚 เอกสารประกอบ

### เอกสารหลัก

1. **[TUTORIAL.md](./TUTORIAL.md)** - คู่มือการสอนแบบ step-by-step (1-100+ ขั้นตอน)
2. **[SUMMARY.md](./SUMMARY.md)** - สรุปภาพรวมระบบและไฟล์ทั้งหมด
3. **[TASK.md](./TASK.md)** - รายการงานและความรับผิดชอบ
4. **[CHECKLIST.md](./CHECKLIST.md)** - รายการตรวจสอบก่อน deployment
5. **[TODO.md](./TODO.md)** - สิ่งที่ต้องทำและ roadmap

### เอกสารแบ่งตามหัวข้อ

- **[PART01.md](./docs/parts/PART01.md)** - พื้นฐานและการติดตั้ง
- **[PART02.md](./docs/parts/PART02.md)** - การตั้งค่า Blockchain Nodes (Geth/Anvil)
- **[PART03.md](./docs/parts/PART03.md)** - Smart Contracts และ Solidity
- **[PART04.md](./docs/parts/PART04.md)** - การออกแบบ Database Schema
- **[PART05.md](./docs/parts/PART05.md)** - Indexer และ ETL System
- **[PART06.md](./docs/parts/PART06.md)** - API Layer และ Backend
- **[PART07.md](./docs/parts/PART07.md)** - Explorer UI และ Frontend
- **[PART08.md](./docs/parts/PART08.md)** - Analytics และ Advanced Features
- **[PART09.md](./docs/parts/PART09.md)** - Monitoring และ Observability
- **[PART10.md](./docs/parts/PART10.md)** - Security Best Practices
- **[PART11.md](./docs/parts/PART11.md)** - Deployment และ DevOps
- **[PART12.md](./docs/parts/PART12.md)** - Testing และ Quality Assurance

---

## 🔧 การพัฒนา

### Local Development

1. **Start dependencies**
```bash
docker-compose up -d postgres redis clickhouse anvil
```

2. **Run backend**
```bash
cd services/api
source venv/bin/activate
uvicorn fastapi_app.main:app --reload
```

3. **Run frontend**
```bash
cd services/ui/nextjs
npm run dev
```

4. **Run indexer**
```bash
cd services/indexer/py
python main.py
```

### Code Style

- **Python**: ใช้ [Black](https://black.readthedocs.io/) และ [isort](https://pycqa.github.io/isort/)
- **TypeScript**: ใช้ [Prettier](https://prettier.io/) และ [ESLint](https://eslint.org/)

```bash
# Format Python code
black .
isort .

# Format TypeScript code
npm run format
npm run lint
```

### Commit Convention

ใช้ [Conventional Commits](https://www.conventionalcommits.org/)

```
feat: เพิ่มฟีเจอร์การค้นหา token
fix: แก้ไข bug ในการแสดงผล transaction
docs: อัปเดตเอกสาร README
style: จัดรูปแบบโค้ด
refactor: ปรับปรุงโครงสร้าง indexer
test: เพิ่ม unit tests สำหรับ API
chore: อัปเดต dependencies
```

---

## 🧪 การทดสอบ

### Unit Tests

```bash
# Backend tests
cd services/api
pytest tests/ -v

# Frontend tests
cd services/ui/nextjs
npm run test
```

### Integration Tests

```bash
# API integration tests
pytest tests/integration/ -v
```

### E2E Tests

```bash
# End-to-end tests
cd tests/e2e
npm run test:e2e
```

### Data Quality Tests

```bash
# Check data consistency
cd tests/data-quality
python check_consistency.py

# Check indexer lag
python check_lag.py
```

### Performance Tests

```bash
# Load testing
cd tests/performance
k6 run load_test.js
```

---

## 🚀 การ Deploy

### Docker Compose (Simple)

```bash
# Production mode
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Kubernetes (Advanced)

```bash
# Using Helm
cd k8s/helm
helm install blockchain-explorer . -n blockchain

# Using kubectl
kubectl apply -k k8s/overlays/production/
```

### Environment Variables

สร้างไฟล์ `.env` จาก `.env.example` และแก้ไขค่าต่อไปนี้:

```env
# Node Configuration
ETH_NODE_URL=https://mainnet.infura.io/v3/YOUR_PROJECT_ID
CHAIN_ID=1

# Database
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=blockchain_explorer
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# API
API_HOST=0.0.0.0
API_PORT=8000
SECRET_KEY=your_secret_key_here

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001
```

---

## ❓ FAQ

### Q: ต้องใช้ full node หรือไม่?
A: ขึ้นอยู่กับความต้องการ สำหรับ production แนะนำให้ใช้ archive node เพื่อเข้าถึง historical data ได้เต็มรูปแบบ สำหรับ development สามารถใช้ anvil หรือ public RPC ได้

### Q: รองรับ blockchain อะไรบ้าง?
A: ปัจจุบันรองรับ Ethereum และ EVM-compatible chains (BSC, Polygon, Arbitrum, etc.) โดยต้องเปลี่ยน RPC endpoint เท่านั้น

### Q: จะ scale ระบบอย่างไร?
A: สามารถ scale ได้หลายวิธี:
- Horizontal scaling: เพิ่ม indexer workers
- Database sharding: แบ่ง data ตาม block range
- Read replicas: ใช้ PostgreSQL replicas สำหรับ read
- Caching: ใช้ Redis cache layer
- Load balancing: ใช้ nginx/HAProxy

### Q: ข้อมูลจะถูกต้องแน่นอนหรือไม่?
A: ระบบมี data quality checks และ reorg handling เพื่อให้มั่นใจว่าข้อมูลตรงกับ blockchain ควรตั้งค่า reorg depth ที่เหมาะสม (เช่น 12 blocks สำหรับ Ethereum)

### Q: ค่าใช้จ่ายในการรันระบบคือเท่าไร?
A: ขึ้นอยู่กับ:
- Node type: Self-hosted (~$100-500/เดือน) vs. RPC service (~$50-200/เดือน)
- Database: ~$50-200/เดือน
- Compute: ~$50-100/เดือน
- รวมประมาณ $150-900/เดือน สำหรับ production

---

## 📞 การสนับสนุน

### Community

- 💬 **Discord**: [Join our Discord](https://discord.gg/example)
- 🐦 **Twitter**: [@blockchain_explorer](https://twitter.com/example)
- 📧 **Email**: support@example.com

### Issues

หากพบปัญหาหรือต้องการขอฟีเจอร์ใหม่ กรุณาสร้าง [GitHub Issue](https://github.com/yourusername/blockchain-explorer/issues)

### Contributing

เรายินดีรับ contributions! กรุณาอ่าน [CONTRIBUTING.md](./CONTRIBUTING.md) ก่อน submit PR

---

## 📄 License

MIT License - ดูรายละเอียดใน [LICENSE](./LICENSE) file

---

## 🙏 Acknowledgments

- [Etherscan](https://etherscan.io/) - แรงบันดาลใจสำหรับ UI/UX
- [Ethereum](https://ethereum.org/) - Blockchain platform
- [Foundry](https://book.getfoundry.sh/) - Development framework
- Community contributors

---

## 🗺️ Roadmap

### Q1 2025
- [ ] Contract verification system
- [ ] Multi-chain support
- [ ] Advanced analytics dashboard
- [ ] Mobile app

### Q2 2025
- [ ] NFT metadata service
- [ ] DeFi protocol analytics
- [ ] GraphQL API
- [ ] WebSocket real-time updates

### Q3 2025
- [ ] MEV analytics
- [ ] Mempool explorer
- [ ] Token approval checker
- [ ] Wallet integration

### Q4 2025
- [ ] AI-powered transaction analysis
- [ ] Custom alerts system
- [ ] Public API marketplace
- [ ] Enterprise features

---

**Built with ❤️ by the Blockchain Explorer Team**

---

> 📖 **เริ่มต้นเรียนรู้**: อ่าน [TUTORIAL.md](./TUTORIAL.md) สำหรับคู่มือแบบละเอียด step-by-step
>
> 🚀 **Quick Start**: รัน `docker-compose up -d` เพื่อเริ่มต้นใช้งานทันที
>
> 📊 **Dashboard**: เข้า http://localhost:3000 หลังจาก start services

---
