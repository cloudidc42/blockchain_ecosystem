# PART 01 - พื้นฐานและการติดตั้ง Blockchain Explorer System

> คู่มือฉบับสมบูรณ์สำหรับการเริ่มต้นสร้าง Blockchain Explorer แบบ Etherscan

**เป้าหมายของบทนี้:**
- เข้าใจพื้นฐาน Blockchain และคำศัพท์สำคัญ
- ติดตั้ง tools และ dependencies ทั้งหมด
- Setup environment สำหรับ development
- เริ่มต้น local blockchain node (Anvil)
- เข้าใจโครงสร้างข้อมูล blockchain

**ระยะเวลา:** 4-6 ชั่วโมง
**ระดับ:** Beginner to Intermediate

---

## 📑 สารบัญ

1. [ทำความเข้าใจ Blockchain](#1-ทำความเข้าใจ-blockchain)
2. [คำศัพท์สำคัญ](#2-คำศัพท์สำคัญ)
3. [ติดตั้ง Docker](#3-ติดตั้ง-docker)
4. [ติดตั้ง Node.js](#4-ติดตั้ง-nodejs)
5. [ติดตั้ง Python](#5-ติดตั้ง-python)
6. [ติดตั้ง Foundry](#6-ติดตั้ง-foundry)
7. [Setup Anvil Local Node](#7-setup-anvil-local-node)
8. [แนะนำ Geth](#8-แนะนำ-geth)
9. [โครงสร้างโปรเจกต์](#9-โครงสร้างโปรเจกต์)
10. [การจัดการ Environment Variables](#10-การจัดการ-environment-variables)
11. [Setup Prometheus & Grafana](#11-setup-prometheus--grafana)
12. [มาตรฐานข้อมูล Blockchain](#12-มาตรฐานข้อมูล-blockchain)
13. [แบบฝึกหัด](#13-แบบฝึกหัด)
14. [เกณฑ์ผ่าน](#14-เกณฑ์ผ่าน)

---

## 1. ทำความเข้าใจ Blockchain

### 1.1 Blockchain คืออะไร?

Blockchain คือ **distributed ledger technology** ที่เก็บข้อมูลในรูปแบบของ blocks ที่เชื่อมโยงกันเป็นลูกโซ่ (chain)

```
📊 แผนภาพ Blockchain Structure

Block 0 (Genesis)          Block 1                Block 2                Block 3
┌─────────────────┐       ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Prev: 0x0000... │◄──────│ Prev: 0xabcd... │◄───│ Prev: 0x1234... │◄───│ Prev: 0x5678... │
│ Hash: 0xabcd... │       │ Hash: 0x1234... │    │ Hash: 0x5678... │    │ Hash: 0x9abc... │
│ Data: Genesis   │       │ Data: Tx1, Tx2  │    │ Data: Tx3, Tx4  │    │ Data: Tx5, Tx6  │
│ Timestamp: T0   │       │ Timestamp: T1   │    │ Timestamp: T2   │    │ Timestamp: T3   │
└─────────────────┘       └─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 1.2 คุณสมบัติสำคัญ

1. **Immutability** - ข้อมูลไม่สามารถแก้ไขหลังจากบันทึกแล้ว
2. **Transparency** - ทุกคนเห็นข้อมูลเดียวกัน
3. **Decentralization** - ไม่มีจุดศูนย์กลางเดียว
4. **Cryptographic Security** - ใช้ cryptography ในการรักษาความปลอดภัย

### 1.3 Ethereum Blockchain

Ethereum เป็น blockchain ที่รองรับ **Smart Contracts** - โปรแกรมที่รันบน blockchain

```
🏗️ Ethereum Architecture

┌────────────────────────────────────────────────────────────┐
│                    Application Layer                        │
│  (DApps, Wallets, Explorers, DEX, NFT Marketplaces)       │
└────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                    Smart Contract Layer                     │
│     (Solidity Contracts, EVM Bytecode, Contract State)    │
└────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                   Consensus Layer (PoS)                     │
│        (Validators, Attestations, Block Proposals)         │
└────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                   Execution Layer (EVM)                     │
│      (Transaction Processing, State Management, Gas)       │
└────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                    Network Layer (P2P)                      │
│          (Node Discovery, Block Propagation, Sync)         │
└────────────────────────────────────────────────────────────┘
```

### 1.4 ทำไมต้องมี Block Explorer?

Block Explorer เป็นเครื่องมือที่ช่วยให้:
- 🔍 **ค้นหา** transactions, blocks, addresses ได้ง่าย
- 📊 **วิเคราะห์** network statistics และ trends
- 👁️ **ตรวจสอบ** smart contract interactions
- 💰 **ติดตาม** token transfers และ balances

---

## 2. คำศัพท์สำคัญ

### 2.1 Blockchain Terms

| คำศัพท์ | ความหมาย | ตัวอย่าง |
|---------|----------|----------|
| **Block** | หน่วยข้อมูลที่เก็บ transactions | Block #18000000 |
| **Transaction (Tx)** | การโอนมูลค่าหรือ data | 0x1234...abcd |
| **Address** | ตำแหน่งของ wallet หรือ contract | 0x742d35Cc... |
| **Hash** | ลายเซ็นดิจิทัลของข้อมูล | 0xabcd1234... |
| **Gas** | ค่าธรรมเนียมในการทำ transaction | 21000 gas |
| **Wei** | หน่วยเล็กสุดของ ETH (1 ETH = 10^18 Wei) | 1000000000000000000 wei |
| **Nonce** | ตัวเลขที่นับจำนวน tx ของ address | 42 |
| **Block Number** | หมายเลขลำดับของ block | 18000000 |
| **Timestamp** | เวลาที่สร้าง block | 1699999999 |

### 2.2 Node Types

```
📡 Node Types

┌─────────────────────────────────────────────────────────────┐
│                        Full Node                             │
│  - เก็บ blockchain data ทั้งหมด                            │
│  - Validate transactions และ blocks                         │
│  - ไม่เก็บ historical state                                 │
│  - Disk: ~500GB, Sync: ~1-2 วัน                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                       Archive Node                           │
│  - เก็บ blockchain + historical state ทั้งหมด              │
│  - รองรับ eth_call ที่ block เก่า                          │
│  - จำเป็นสำหรับ blockchain explorer                         │
│  - Disk: ~12TB+, Sync: ~2-4 สัปดาห์                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        Light Node                            │
│  - เก็บ block headers เท่านั้น                             │
│  - ต้องพึ่งพา full nodes                                     │
│  - Disk: ~400MB, Sync: นาที                                 │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Transaction Types

1. **Regular Transfer** - โอน ETH จาก address หนึ่งไปอีก address
2. **Contract Deployment** - สร้าง smart contract ใหม่
3. **Contract Interaction** - เรียกใช้ function ใน smart contract
4. **Internal Transaction** - transaction ที่เกิดจาก contract execution

### 2.4 Smart Contract Standards

| Standard | ชนิด | ใช้สำหรับ | ตัวอย่าง |
|----------|------|-----------|----------|
| **ERC-20** | Fungible Token | เหรียญ, token เหมือนกันทุกตัว | USDT, LINK |
| **ERC-721** | NFT | สินทรัพย์ดิจิทัลที่ไม่เหมือนกัน | CryptoPunks, BAYC |
| **ERC-1155** | Multi-Token | รวม fungible + NFT | Gaming items |
| **ERC-4626** | Tokenized Vault | Yield-bearing tokens | Yearn vaults |

---

## 3. ติดตั้ง Docker

Docker เป็น platform สำหรับ containerization ที่เราจะใช้รัน services ทั้งหมด

### 3.1 ติดตั้ง Docker บน Linux

```bash
# 1. Update package index
sudo apt-get update

# 2. Install prerequisites
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 3. Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 4. Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io \
    docker-buildx-plugin docker-compose-plugin

# 6. Verify installation
docker --version
docker compose version

# 7. Add user to docker group (ไม่ต้องใช้ sudo)
sudo usermod -aG docker $USER
newgrp docker

# 8. Test Docker
docker run hello-world
```

### 3.2 ติดตั้ง Docker บน macOS

```bash
# 1. ดาวน์โหลด Docker Desktop จาก:
# https://www.docker.com/products/docker-desktop

# 2. ติดตั้ง Docker Desktop.app

# 3. เปิด Docker Desktop

# 4. ตรวจสอบ
docker --version
docker compose version
```

### 3.3 ติดตั้ง Docker บน Windows

```powershell
# 1. Install WSL 2
wsl --install

# 2. ดาวน์โหลด Docker Desktop จาก:
# https://www.docker.com/products/docker-desktop

# 3. ติดตั้งและเปิด Docker Desktop

# 4. ตรวจสอบ (ใน PowerShell)
docker --version
docker compose version
```

### 3.4 Docker Commands พื้นฐาน

```bash
# ดู images ที่มี
docker images

# ดู containers ที่รันอยู่
docker ps

# ดู containers ทั้งหมด (รวม stopped)
docker ps -a

# รัน container
docker run -d --name my-container nginx

# หยุด container
docker stop my-container

# ลบ container
docker rm my-container

# ดู logs
docker logs my-container

# เข้าไปใน container
docker exec -it my-container bash

# ลบ images
docker rmi nginx

# ลบทุกอย่างที่ไม่ใช้แล้ว
docker system prune -a
```

### 3.5 Docker Compose Commands

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# View logs of specific service
docker compose logs -f indexer

# Restart service
docker compose restart indexer

# Rebuild and start
docker compose up -d --build

# View running services
docker compose ps

# Execute command in service
docker compose exec api bash
```

---

## 4. ติดตั้ง Node.js

Node.js จำเป็นสำหรับ frontend (Next.js) และ TypeScript tooling

### 4.1 ติดตั้ง Node.js บน Linux/macOS

```bash
# วิธีที่ 1: ใช้ nvm (แนะนำ)
# 1. ติดตั้ง nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash

# 2. Reload shell
source ~/.bashrc  # หรือ ~/.zshrc สำหรับ zsh

# 3. ติดตั้ง Node.js LTS
nvm install 20
nvm use 20
nvm alias default 20

# 4. ตรวจสอบ
node --version   # ควรได้ v20.x.x
npm --version    # ควรได้ v10.x.x

# วิธีที่ 2: ติดตั้งตรงจาก package manager (Ubuntu/Debian)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# วิธีที่ 3: ติดตั้งบน macOS ด้วย Homebrew
brew install node@20
```

### 4.2 ติดตั้ง Node.js บน Windows

```powershell
# วิธีที่ 1: ดาวน์โหลด installer จาก
# https://nodejs.org/

# วิธีที่ 2: ใช้ Chocolatey
choco install nodejs-lts

# ตรวจสอบ
node --version
npm --version
```

### 4.3 Node.js Tools

```bash
# Install yarn (alternative package manager)
npm install -g yarn

# Install pnpm (faster package manager)
npm install -g pnpm

# Install TypeScript
npm install -g typescript

# Install ts-node (run TypeScript directly)
npm install -g ts-node

# ตรวจสอบ
yarn --version
pnpm --version
tsc --version
ts-node --version
```

---

## 5. ติดตั้ง Python

Python จำเป็นสำหรับ backend (FastAPI) และ indexer

### 5.1 ติดตั้ง Python บน Linux

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv python3.11-dev

# หรือติดตั้งจาก deadsnakes PPA (สำหรับ Python version ใหม่)
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv python3.11-dev

# ตั้งเป็น default
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# ติดตั้ง pip
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# ตรวจสอบ
python3 --version  # ควรได้ Python 3.11.x
pip3 --version
```

### 5.2 ติดตั้ง Python บน macOS

```bash
# ใช้ Homebrew
brew install python@3.11

# Add to PATH
echo 'export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# ตรวจสอบ
python3 --version
pip3 --version
```

### 5.3 ติดตั้ง Python บน Windows

```powershell
# วิธีที่ 1: ดาวน์โหลดจาก python.org
# https://www.python.org/downloads/

# วิธีที่ 2: ใช้ Chocolatey
choco install python311

# ตรวจสอบ
python --version
pip --version
```

### 5.4 Python Virtual Environment

```bash
# สร้าง virtual environment
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
.\venv\Scripts\activate

# ติดตั้ง packages
pip install web3 sqlalchemy fastapi uvicorn

# Save dependencies
pip freeze > requirements.txt

# Install from requirements.txt
pip install -r requirements.txt

# Deactivate
deactivate
```

### 5.5 Python Tools

```bash
# Install useful tools
pip install black isort pylint mypy pytest pytest-cov

# Black - Code formatter
black .

# isort - Import sorter
isort .

# pylint - Linter
pylint services/

# mypy - Type checker
mypy services/

# pytest - Testing
pytest tests/ -v
pytest tests/ --cov=services/
```

---

## 6. ติดตั้ง Foundry

Foundry เป็น toolkit สำหรับพัฒนา Ethereum ที่เร็วและทรงพลัง

### 6.1 ติดตั้ง Foundry

```bash
# ติดตั้ง Foundry
curl -L https://foundry.paradigm.xyz | bash

# Reload shell หรือ run:
source ~/.bashrc  # หรือ ~/.zshrc

# Install foundry tools
foundryup

# ตรวจสอบ
forge --version
anvil --version
cast --version
chisel --version
```

### 6.2 Foundry Tools

```
🔨 Foundry Toolkit

┌────────────────────────────────────────────────────────┐
│                      FORGE                              │
│  - Build, test, deploy smart contracts                 │
│  - ใช้งาน: forge build, forge test, forge script      │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│                      ANVIL                              │
│  - Local Ethereum node for testing                     │
│  - ใช้งาน: anvil --port 8545                          │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│                       CAST                              │
│  - CLI tool for Ethereum RPC calls                     │
│  - ใช้งาน: cast call, cast send, cast block          │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│                      CHISEL                             │
│  - Solidity REPL for quick testing                     │
│  - ใช้งาน: chisel                                     │
└────────────────────────────────────────────────────────┘
```

### 6.3 Foundry Commands

```bash
# สร้างโปรเจกต์ใหม่
forge init my-project
cd my-project

# Build contracts
forge build

# Run tests
forge test
forge test -vv  # verbose
forge test -vvvv  # very verbose

# Deploy contract
forge create src/MyContract.sol:MyContract \
    --rpc-url http://localhost:8545 \
    --private-key 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80

# Format code
forge fmt

# Generate documentation
forge doc

# Check gas usage
forge test --gas-report
```

---

## 7. Setup Anvil Local Node

Anvil คือ local Ethereum node ที่ดีสำหรับการพัฒนา

### 7.1 เริ่มต้น Anvil

```bash
# Start Anvil (แบบพื้นฐาน)
anvil

# Start พร้อม options
anvil \
    --port 8545 \
    --chain-id 31337 \
    --accounts 10 \
    --balance 10000

# Fork mainnet
anvil --fork-url https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY

# Fork ที่ block เฉพาะ
anvil \
    --fork-url https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY \
    --fork-block-number 18000000
```

### 7.2 Anvil Output

เมื่อ start Anvil คุณจะเห็น:

```
                             _   _
                            (_) | |
      __ _   _ __   __   __  _  | |
     / _` | | '_ \  \ \ / / | | | |
    | (_| | | | | |  \ V /  | | | |
     \__,_| |_| |_|   \_/   |_| |_|

    0.2.0 (a1b2c3d 2024-01-01T00:00:00.000000000Z)
    https://github.com/foundry-rs/foundry

Available Accounts
==================
(0) 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 (10000.000000000000000000 ETH)
(1) 0x70997970C51812dc3A010C7d01b50e0d17dc79C8 (10000.000000000000000000 ETH)
(2) 0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC (10000.000000000000000000 ETH)
...

Private Keys
==================
(0) 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
(1) 0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d
(2) 0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a
...

Wallet
==================
Mnemonic:          test test test test test test test test test test test junk
Derivation path:   m/44'/60'/0'/0/

Chain ID
==================
31337

Base Fee
==================
1000000000

Gas Limit
==================
30000000

Genesis Timestamp
==================
1699999999

Listening on 127.0.0.1:8545
```

### 7.3 ทดสอบ Anvil

```bash
# ติดตั้ง curl (ถ้ายังไม่มี)
sudo apt-get install curl

# Test 1: Get chain ID
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":1}'

# Expected: {"jsonrpc":"2.0","id":1,"result":"0x7a69"}

# Test 2: Get latest block number
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'

# Test 3: Get account balance
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"eth_getBalance",
    "params":["0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266", "latest"],
    "id":1
  }'
```

### 7.4 ใช้งาน Anvil ด้วย Python

```python
# install: pip install web3

from web3 import Web3

# เชื่อมต่อ Anvil
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

# ตรวจสอบการเชื่อมต่อ
if w3.is_connected():
    print("✅ Connected to Anvil")

    # Get chain ID
    chain_id = w3.eth.chain_id
    print(f"Chain ID: {chain_id}")

    # Get latest block
    latest_block = w3.eth.block_number
    print(f"Latest block: {latest_block}")

    # Get account balance
    account = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
    balance = w3.eth.get_balance(account)
    balance_eth = w3.from_wei(balance, 'ether')
    print(f"Balance: {balance_eth} ETH")

    # Send transaction
    tx_hash = w3.eth.send_transaction({
        'from': account,
        'to': '0x70997970C51812dc3A010C7d01b50e0d17dc79C8',
        'value': w3.to_wei(1, 'ether'),
        'gas': 21000,
        'gasPrice': w3.eth.gas_price
    })
    print(f"Transaction hash: {tx_hash.hex()}")
else:
    print("❌ Not connected")
```

### 7.5 Anvil Scripts

สร้างไฟล์ `scripts/start-anvil.sh`:

```bash
#!/bin/bash

# Start Anvil with custom settings

echo "🚀 Starting Anvil..."

anvil \
    --host 0.0.0.0 \
    --port 8545 \
    --chain-id 31337 \
    --accounts 20 \
    --balance 10000 \
    --gas-limit 30000000 \
    --gas-price 1 \
    --block-time 2 \
    --steps-tracing \
    --state-interval 10

# Options explained:
# --host: Listen on all interfaces
# --port: RPC port
# --chain-id: Chain identifier
# --accounts: Number of accounts to generate
# --balance: Initial balance for each account (ETH)
# --gas-limit: Block gas limit
# --gas-price: Gas price in gwei
# --block-time: Seconds between blocks (0 = instant)
# --steps-tracing: Enable step-level tracing
# --state-interval: Interval for saving state snapshots
```

ให้สิทธิ์ execute:

```bash
chmod +x scripts/start-anvil.sh
./scripts/start-anvil.sh
```

---

## 8. แนะนำ Geth

Geth (Go Ethereum) คือ official Ethereum client เขียนด้วย Go

### 8.1 Geth vs Anvil

```
📊 Geth vs Anvil Comparison

┌─────────────────────┬──────────────────┬──────────────────┐
│     Feature         │      Anvil       │      Geth        │
├─────────────────────┼──────────────────┼──────────────────┤
│ Use Case            │ Development      │ Production       │
│ Speed               │ Very Fast        │ Normal           │
│ Real Blockchain     │ No               │ Yes              │
│ Storage Required    │ ~100MB           │ ~500GB - 12TB    │
│ Sync Time           │ Instant          │ Hours - Weeks    │
│ Fork Mainnet        │ Yes (easy)       │ N/A              │
│ Mining/Consensus    │ Instant/None     │ PoS              │
│ Cost                │ Free             │ Free + Hardware  │
└─────────────────────┴──────────────────┴──────────────────┘
```

### 8.2 เมื่อไหร่ใช้ Geth?

ใช้ Geth เมื่อ:
- ✅ ต้องการ production-ready node
- ✅ ต้องการ archive node สำหรับ historical data
- ✅ ต้องการ sync กับ mainnet/testnet จริง
- ✅ ต้องการ high reliability และ uptime

ใช้ Anvil เมื่อ:
- ✅ กำลังพัฒนาและทดสอบ
- ✅ ต้องการ fast iteration
- ✅ ไม่ต้องการใช้ disk มาก
- ✅ ต้องการ fork mainnet เพื่อทดสอบ

### 8.3 ติดตั้ง Geth

```bash
# Ubuntu/Debian
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install ethereum

# macOS
brew tap ethereum/ethereum
brew install ethereum

# ตรวจสอบ
geth version
```

### 8.4 Start Geth (Sepolia Testnet)

```bash
# Start Geth on Sepolia testnet
geth \
    --sepolia \
    --http \
    --http.addr 0.0.0.0 \
    --http.port 8545 \
    --http.corsdomain "*" \
    --http.api "eth,net,web3,txpool" \
    --ws \
    --ws.addr 0.0.0.0 \
    --ws.port 8546 \
    --ws.origins "*" \
    --ws.api "eth,net,web3,txpool" \
    --syncmode snap \
    --datadir ./geth-data

# For Archive Node (mainnet):
geth \
    --mainnet \
    --http \
    --http.addr 0.0.0.0 \
    --http.port 8545 \
    --http.api "eth,net,web3,debug,trace" \
    --ws \
    --ws.addr 0.0.0.0 \
    --ws.port 8546 \
    --ws.api "eth,net,web3,debug,trace" \
    --syncmode full \
    --gcmode archive \
    --datadir ./geth-archive \
    --cache 8192 \
    --maxpeers 50
```

### 8.5 Geth Console

```bash
# Attach to running Geth
geth attach http://localhost:8545

# In console:
> eth.blockNumber
18000000

> eth.getBalance("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb")
1234567890000000000

> web3.fromWei(eth.getBalance("0x742d35Cc..."), "ether")
1.23456789

> eth.syncing
{
  currentBlock: 17500000,
  highestBlock: 18000000,
  knownStates: 950000000,
  pulledStates: 900000000,
  startingBlock: 0
}

> exit
```

---

## 9. โครงสร้างโปรเจกต์

### 9.1 สร้างโครงสร้างโปรเจกต์

```bash
# สร้าง root directory
mkdir blockchain-explorer
cd blockchain-explorer

# สร้างโครงสร้างแบบเต็ม
mkdir -p \
    docs/{parts,architecture,api,guides} \
    services/{geth,anvil,indexer/{py,ts},api/fastapi_app,ui/nextjs,observability/{prometheus,grafana}} \
    db/{postgres,clickhouse} \
    contracts/{src,test,script,lib} \
    tests/{e2e,data-quality,retrieval-metrics} \
    k8s/{base,overlays/{development,staging,production},helm} \
    scripts

# สร้างไฟล์พื้นฐาน
touch .env.example .gitignore README.md docker-compose.yml

# ตรวจสอบโครงสร้าง
tree -L 3
```

### 9.2 โครงสร้างแบบละเอียด

```
blockchain-explorer/
│
├── 📄 README.md                        # เอกสารหลัก
├── 📄 docker-compose.yml               # Docker orchestration
├── 📄 .env.example                     # Environment template
├── 📄 .gitignore                       # Git ignore rules
│
├── 📂 docs/                            # เอกสาร
│   ├── 📂 parts/                       # เอกสารแบ่งส่วน
│   │   ├── PART01.md                   # ไฟล์นี้
│   │   ├── PART02.md
│   │   └── ...
│   ├── 📂 architecture/                # แผนภาพสถาปัตยกรรม
│   ├── 📂 api/                         # API docs
│   └── 📂 guides/                      # คำแนะนำเพิ่มเติม
│
├── 📂 services/                        # Services หลัก
│   ├── 📂 geth/                        # Geth node
│   │   ├── Dockerfile
│   │   ├── entrypoint.sh
│   │   └── config.toml
│   │
│   ├── 📂 anvil/                       # Anvil node
│   │   ├── Dockerfile
│   │   └── start.sh
│   │
│   ├── 📂 indexer/                     # Indexer services
│   │   ├── 📂 py/                      # Python indexer
│   │   │   ├── main.py
│   │   │   ├── requirements.txt
│   │   │   └── ...
│   │   └── 📂 ts/                      # TypeScript indexer
│   │       └── ...
│   │
│   ├── 📂 api/                         # Backend API
│   │   └── 📂 fastapi_app/
│   │       ├── main.py
│   │       ├── requirements.txt
│   │       ├── 📂 routers/
│   │       ├── 📂 models/
│   │       └── ...
│   │
│   ├── 📂 ui/                          # Frontend
│   │   └── 📂 nextjs/
│   │       ├── package.json
│   │       ├── 📂 app/
│   │       ├── 📂 components/
│   │       └── ...
│   │
│   └── 📂 observability/               # Monitoring
│       ├── 📂 prometheus/
│       └── 📂 grafana/
│
├── 📂 db/                              # Database schemas
│   ├── 📂 postgres/
│   │   ├── init.sql
│   │   ├── schema.sql
│   │   └── indexes.sql
│   └── 📂 clickhouse/
│       └── ...
│
├── 📂 contracts/                       # Smart contracts
│   ├── foundry.toml
│   ├── 📂 src/                         # Contract source
│   ├── 📂 test/                        # Tests
│   ├── 📂 script/                      # Deployment scripts
│   └── 📂 lib/                         # Dependencies
│
├── 📂 tests/                           # Tests
│   ├── 📂 e2e/                         # End-to-end tests
│   ├── 📂 data-quality/                # Data quality tests
│   └── 📂 retrieval-metrics/           # Search tests
│
├── 📂 k8s/                             # Kubernetes (optional)
│   ├── 📂 base/
│   ├── 📂 overlays/
│   └── 📂 helm/
│
└── 📂 scripts/                         # Utility scripts
    ├── setup.sh
    ├── start-anvil.sh
    ├── backup-db.sh
    └── ...
```

### 9.3 สร้างไฟล์ README.md

```bash
cat > README.md << 'EOF'
# Blockchain Explorer System

> Full-stack Blockchain Explorer like Etherscan

## Quick Start

```bash
# 1. Clone and setup
git clone <repo>
cd blockchain-explorer
cp .env.example .env

# 2. Start services
docker-compose up -d

# 3. Access
- UI: http://localhost:3000
- API: http://localhost:8000/docs
- Grafana: http://localhost:3001
```

## Documentation

- [PART01 - Setup](./docs/parts/PART01.md)
- [Full Documentation](./docs/)

## Tech Stack

- **Blockchain**: Geth, Anvil
- **Backend**: Python, FastAPI
- **Frontend**: Next.js, React
- **Database**: PostgreSQL, ClickHouse, Redis
- **Monitoring**: Prometheus, Grafana

## License

MIT
EOF
```

---

## 10. การจัดการ Environment Variables

### 10.1 สร้างไฟล์ .env.example

ไฟล์นี้ถูกสร้างไว้แล้วในโปรเจกต์ ตรวจสอบที่ `/.env.example`

### 10.2 สร้าง .env สำหรับ Development

```bash
# Copy from example
cp .env.example .env

# Edit values
nano .env
```

ค่าที่ควรเปลี่ยนสำหรับ development:

```bash
# Blockchain
ETH_NODE_URL=http://anvil:8545
CHAIN_ID=31337

# Database - ใช้ default passwords ใน dev
POSTGRES_PASSWORD=postgres
CLICKHOUSE_PASSWORD=clickhouse
REDIS_PASSWORD=redis

# API
SECRET_KEY=$(openssl rand -hex 32)

# Log Level
LOG_LEVEL=DEBUG
```

### 10.3 Environment per Stage

```
📊 Environment Strategy

Development (.env.development)
├── Local databases
├── Anvil node
├── DEBUG logging
└── No authentication

Staging (.env.staging)
├── Cloud databases
├── Sepolia testnet
├── INFO logging
└── Basic authentication

Production (.env.production)
├── Production databases
├── Mainnet (archive node)
├── WARNING logging
└── Full authentication + rate limiting
```

### 10.4 การจัดการ Secrets

```bash
# ❌ NEVER commit .env files
echo ".env" >> .gitignore
echo ".env.*" >> .gitignore
echo "!.env.example" >> .gitignore

# ✅ Use environment-specific files
cp .env.example .env.development
cp .env.example .env.staging
cp .env.example .env.production

# Load environment
# In Python:
from dotenv import load_dotenv
load_dotenv('.env.development')

# In Node.js:
require('dotenv').config({ path: '.env.development' })
```

---

## 11. Setup Prometheus & Grafana

### 11.1 สร้าง Prometheus Config

```bash
mkdir -p services/observability/prometheus
cat > services/observability/prometheus/prometheus.yml << 'EOF'
# Prometheus Configuration

global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'blockchain-explorer'
    environment: 'development'

# Alert Manager (optional)
# alerting:
#   alertmanagers:
#     - static_configs:
#         - targets: ['alertmanager:9093']

# Load rules
rule_files:
  - 'alerts.yml'
  # - 'recording-rules.yml'

# Scrape configs
scrape_configs:
  # Prometheus itself
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Indexer
  - job_name: 'indexer'
    static_configs:
      - targets: ['indexer:9000']
    metrics_path: '/metrics'

  # API
  - job_name: 'api'
    static_configs:
      - targets: ['api:8000']
    metrics_path: '/metrics'

  # PostgreSQL Exporter (optional)
  # - job_name: 'postgres'
  #   static_configs:
  #     - targets: ['postgres-exporter:9187']

  # Redis Exporter (optional)
  # - job_name: 'redis'
  #   static_configs:
  #     - targets: ['redis-exporter:9121']

  # Node Exporter for system metrics (optional)
  # - job_name: 'node'
  #   static_configs:
  #     - targets: ['node-exporter:9100']
EOF
```

### 11.2 สร้าง Prometheus Alerts

```bash
cat > services/observability/prometheus/alerts.yml << 'EOF'
# Alert Rules

groups:
  - name: blockchain_explorer
    interval: 30s
    rules:
      # Indexer lag alert
      - alert: IndexerLagHigh
        expr: indexer_lag_seconds > 60
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Indexer lag is high"
          description: "Indexer is {{ $value }} seconds behind chain head"

      # API error rate alert
      - alert: APIErrorRateHigh
        expr: rate(api_requests_total{status=~"5.."}[5m]) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "API error rate is high"
          description: "API error rate is {{ $value }} (threshold: 0.01)"

      # Service down alert
      - alert: ServiceDown
        expr: up == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} is down"
          description: "{{ $labels.job }} has been down for more than 2 minutes"

      # Database disk space alert
      - alert: DatabaseDiskSpaceLow
        expr: (node_filesystem_avail_bytes{mountpoint="/var/lib/postgresql"} / node_filesystem_size_bytes{mountpoint="/var/lib/postgresql"}) < 0.2
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Database disk space is low"
          description: "Only {{ $value | humanizePercentage }} disk space remaining"
EOF
```

### 11.3 สร้าง Grafana Datasource

```bash
mkdir -p services/observability/grafana
cat > services/observability/grafana/datasources.yml << 'EOF'
# Grafana Datasources

apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
    jsonData:
      timeInterval: "15s"

  # ClickHouse datasource (requires plugin)
  # - name: ClickHouse
  #   type: vertamedia-clickhouse-datasource
  #   access: proxy
  #   url: http://clickhouse:8123
  #   database: blockchain_analytics
  #   jsonData:
  #     username: default
  #   secureJsonData:
  #     password: clickhouse
EOF
```

### 11.4 สร้าง Grafana Dashboard

```bash
mkdir -p services/observability/grafana/dashboards

# Dashboard provisioning config
cat > services/observability/grafana/dashboards/dashboards.yml << 'EOF'
apiVersion: 1

providers:
  - name: 'Blockchain Explorer'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards
EOF

# Simple dashboard JSON
cat > services/observability/grafana/dashboards/overview.json << 'EOF'
{
  "dashboard": {
    "title": "Blockchain Explorer Overview",
    "panels": [
      {
        "title": "Latest Block Number",
        "targets": [
          {
            "expr": "indexer_latest_block"
          }
        ]
      },
      {
        "title": "Indexer Lag",
        "targets": [
          {
            "expr": "indexer_lag_seconds"
          }
        ]
      },
      {
        "title": "API Request Rate",
        "targets": [
          {
            "expr": "rate(api_requests_total[5m])"
          }
        ]
      }
    ]
  }
}
EOF
```

---

## 12. มาตรฐานข้อมูล Blockchain

### 12.1 โครงสร้าง Block

```python
# Block structure
{
    "number": 18000000,                    # Block number
    "hash": "0xabcd1234...",               # Block hash (32 bytes)
    "parentHash": "0x5678efgh...",         # Previous block hash
    "timestamp": 1699999999,               # Unix timestamp
    "miner": "0x742d35Cc...",              # Block proposer/miner
    "difficulty": 0,                        # Difficulty (0 for PoS)
    "totalDifficulty": "58750003716598352816469",
    "gasLimit": 30000000,                  # Max gas per block
    "gasUsed": 15234567,                   # Gas used in this block
    "baseFeePerGas": 20000000000,          # Base fee (EIP-1559)
    "extraData": "0x...",                  # Extra data
    "size": 123456,                        # Block size in bytes
    "transactions": [                       # List of tx hashes
        "0xtxhash1...",
        "0xtxhash2..."
    ],
    "transactionsRoot": "0x...",           # Merkle root of txs
    "stateRoot": "0x...",                  # State trie root
    "receiptsRoot": "0x...",               # Receipts trie root
    "logsBloom": "0x...",                  # Bloom filter for logs
    "nonce": "0x0000000000000000",         # Nonce (PoS = 0)
    "mixHash": "0x...",                    # Mix hash
    "sha3Uncles": "0x...",                 # Uncles hash
    "uncles": []                           # Uncle blocks (usually empty in PoS)
}
```

### 12.2 โครงสร้าง Transaction

```python
# Transaction structure
{
    "hash": "0xtxhash...",                 # Transaction hash
    "nonce": 42,                           # Sender's nonce
    "blockHash": "0xblock...",             # Block containing this tx
    "blockNumber": 18000000,               # Block number
    "transactionIndex": 123,               # Position in block
    "from": "0xsender...",                 # Sender address
    "to": "0xrecipient...",                # Recipient (null for contract creation)
    "value": "1000000000000000000",        # Value in Wei (1 ETH)
    "gas": 21000,                          # Gas limit
    "gasPrice": "20000000000",             # Gas price (legacy)
    "maxFeePerGas": "30000000000",         # Max fee (EIP-1559)
    "maxPriorityFeePerGas": "2000000000", # Max priority fee (EIP-1559)
    "input": "0x...",                      # Transaction data
    "v": "0x26",                           # Signature V
    "r": "0x...",                          # Signature R
    "s": "0x...",                          # Signature S
    "type": "0x2",                         # Transaction type (0x2 = EIP-1559)
    "chainId": "0x1"                       # Chain ID
}
```

### 12.3 โครงสร้าง Transaction Receipt

```python
# Transaction receipt
{
    "transactionHash": "0xtxhash...",
    "transactionIndex": 123,
    "blockHash": "0xblock...",
    "blockNumber": 18000000,
    "from": "0xsender...",
    "to": "0xrecipient...",
    "cumulativeGasUsed": 5234567,          # Total gas used up to this tx
    "gasUsed": 21000,                      # Gas used by this tx
    "contractAddress": null,               # New contract address (if creation)
    "logs": [                              # Event logs
        {
            "address": "0xcontract...",
            "topics": [
                "0xeventhash...",          # Event signature
                "0xparam1...",             # Indexed parameter 1
                "0xparam2..."              # Indexed parameter 2
            ],
            "data": "0x...",               # Non-indexed data
            "blockNumber": 18000000,
            "transactionHash": "0xtxhash...",
            "transactionIndex": 123,
            "blockHash": "0xblock...",
            "logIndex": 456,
            "removed": false
        }
    ],
    "logsBloom": "0x...",
    "status": "0x1",                       # 1 = success, 0 = failed
    "effectiveGasPrice": "22000000000",    # Actual gas price paid
    "type": "0x2"
}
```

### 12.4 โครงสร้าง Event Log

```python
# Event log (from receipt.logs)
{
    "address": "0xcontract...",            # Contract that emitted
    "topics": [
        "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",  # Transfer(address,address,uint256)
        "0x000000000000000000000000sender...",   # from (indexed)
        "0x000000000000000000000000recipient..." # to (indexed)
    ],
    "data": "0x00000000000000000000000000000000000000000000000de0b6b3a7640000",  # amount
    "blockNumber": 18000000,
    "transactionHash": "0xtxhash...",
    "transactionIndex": 123,
    "blockHash": "0xblock...",
    "logIndex": 456,
    "removed": false                       # true if reorg removed this log
}
```

### 12.5 ตัวอย่าง: Decode Event Log

```python
from web3 import Web3

# ERC-20 Transfer event
# event Transfer(address indexed from, address indexed to, uint256 value)

# Event signature hash
transfer_signature = Web3.keccak(text="Transfer(address,address,uint256)").hex()
print(f"Transfer signature: {transfer_signature}")
# 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef

# Decode log
log = {
    "topics": [
        "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
        "0x000000000000000000000000f39fd6e51aad88f6f4ce6ab8827279cfffb92266",
        "0x00000000000000000000000070997970c51812dc3a010c7d01b50e0d17dc79c8"
    ],
    "data": "0x0000000000000000000000000000000000000000000000000de0b6b3a7640000"
}

# Parse
from_address = "0x" + log["topics"][1][-40:]
to_address = "0x" + log["topics"][2][-40:]
amount_wei = int(log["data"], 16)
amount_eth = amount_wei / 10**18

print(f"From: {from_address}")
print(f"To: {to_address}")
print(f"Amount: {amount_eth} tokens")
```

---

## 13. แบบฝึกหัด

### แบบฝึกหัดที่ 1: ติดตั้ง Tools

**เป้าหมาย:** ติดตั้ง Docker, Node.js, Python, Foundry ให้สมบูรณ์

**ขั้นตอน:**
1. ติดตั้ง Docker และรัน `docker run hello-world`
2. ติดตั้ง Node.js และตรวจสอบ `node --version` (ต้องได้ v20+)
3. ติดตั้ง Python และตรวจสอบ `python3 --version` (ต้องได้ v3.11+)
4. ติดตั้ง Foundry และตรวจสอบ `forge --version`

**เกณฑ์ผ่าน:**
- ✅ ทุก command ทำงานได้โดยไม่ error
- ✅ Version ตรงตามที่กำหนด

---

### แบบฝึกหัดที่ 2: Start Anvil และทดสอบ

**เป้าหมาย:** เริ่ม Anvil และทดสอบ RPC calls

**ขั้นตอน:**

1. Start Anvil:
```bash
anvil --port 8545
```

2. ทดสอบด้วย curl:
```bash
# Test 1: Chain ID
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":1}'

# Test 2: Block number
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'

# Test 3: Get balance
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"eth_getBalance",
    "params":["0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266", "latest"],
    "id":1
  }'
```

**เกณฑ์ผ่าน:**
- ✅ Anvil start สำเร็จ
- ✅ ทุก RPC call ได้ response ที่ถูกต้อง
- ✅ Balance ของ account แรก = 10000 ETH

---

### แบบฝึกหัดที่ 3: Python Web3 Connection

**เป้าหมาย:** เชื่อมต่อ Anvil ด้วย Python

**ขั้นตอน:**

1. ติดตั้ง web3.py:
```bash
pip install web3
```

2. สร้างไฟล์ `test_connection.py`:
```python
from web3 import Web3

# Connect to Anvil
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

# Test connection
if w3.is_connected():
    print("✅ Connected to Anvil")

    # Get chain ID
    chain_id = w3.eth.chain_id
    print(f"Chain ID: {chain_id}")
    assert chain_id == 31337, "Chain ID should be 31337"

    # Get latest block
    latest_block = w3.eth.block_number
    print(f"Latest block: {latest_block}")

    # Get account balance
    account = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
    balance = w3.eth.get_balance(account)
    balance_eth = w3.from_wei(balance, 'ether')
    print(f"Balance: {balance_eth} ETH")
    assert balance_eth == 10000, "Balance should be 10000 ETH"

    print("\n✅ All tests passed!")
else:
    print("❌ Not connected")
    exit(1)
```

3. รัน:
```bash
python test_connection.py
```

**เกณฑ์ผ่าน:**
- ✅ Connection สำเร็จ
- ✅ Chain ID = 31337
- ✅ Balance = 10000 ETH
- ✅ ทุก assertion ผ่าน

---

### แบบฝึกหัดที่ 4: Send Transaction

**เป้าหมาย:** ส่ง transaction บน Anvil

**ขั้นตอน:**

สร้างไฟล์ `send_transaction.py`:
```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

# Accounts (from Anvil output)
account1 = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
account2 = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
private_key1 = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

print("Before transaction:")
print(f"Account 1: {w3.from_wei(w3.eth.get_balance(account1), 'ether')} ETH")
print(f"Account 2: {w3.from_wei(w3.eth.get_balance(account2), 'ether')} ETH")

# Build transaction
tx = {
    'from': account1,
    'to': account2,
    'value': w3.to_wei(1, 'ether'),
    'gas': 21000,
    'gasPrice': w3.eth.gas_price,
    'nonce': w3.eth.get_transaction_count(account1),
    'chainId': 31337
}

# Sign transaction
signed_tx = w3.eth.account.sign_transaction(tx, private_key1)

# Send transaction
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(f"\n📤 Transaction sent: {tx_hash.hex()}")

# Wait for receipt
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"✅ Transaction mined in block {receipt['blockNumber']}")
print(f"   Gas used: {receipt['gasUsed']}")
print(f"   Status: {'Success' if receipt['status'] == 1 else 'Failed'}")

print("\nAfter transaction:")
print(f"Account 1: {w3.from_wei(w3.eth.get_balance(account1), 'ether')} ETH")
print(f"Account 2: {w3.from_wei(w3.eth.get_balance(account2), 'ether')} ETH")
```

รัน:
```bash
python send_transaction.py
```

**เกณฑ์ผ่าน:**
- ✅ Transaction ส่งสำเร็จ
- ✅ ได้ transaction hash
- ✅ Receipt status = 1 (success)
- ✅ Balance เปลี่ยนแปลงถูกต้อง

---

### แบบฝึกหัดที่ 5: Setup Project Structure

**เป้าหมาย:** สร้างโครงสร้างโปรเจกต์ครบถ้วน

**ขั้นตอน:**

1. Clone repository (หรือสร้างใหม่)
2. สร้างโครงสร้าง folders ตาม section 9
3. สร้าง `.env` จาก `.env.example`
4. แก้ไขค่าใน `.env` สำหรับ development

**เกณฑ์ผ่าน:**
- ✅ มี folders ครบตามโครงสร้าง
- ✅ มีไฟล์ `.env` ที่กำหนดค่าแล้ว
- ✅ มีไฟล์ `README.md` พื้นฐาน
- ✅ Git initialized และ `.gitignore` ครบถ้วน

---

## 14. เกณฑ์ผ่าน

เพื่อผ่านบท PART01 นี้ คุณต้อง:

### ✅ Knowledge Check

- [ ] เข้าใจคำศัพท์ blockchain พื้นฐาน (block, transaction, address, gas)
- [ ] เข้าใจความแตกต่างระหว่าง full node และ archive node
- [ ] เข้าใจ transaction types และ event logs
- [ ] รู้จัก ERC token standards (ERC-20, ERC-721, ERC-1155)

### ✅ Technical Setup

- [ ] ติดตั้ง Docker และ Docker Compose สำเร็จ
- [ ] ติดตั้ง Node.js 20+ สำเร็จ
- [ ] ติดตั้ง Python 3.11+ สำเร็จ
- [ ] ติดตั้ง Foundry สำเร็จ
- [ ] Start Anvil และทดสอบ RPC calls ได้
- [ ] เชื่อมต่อ Anvil ด้วย Python web3.py ได้
- [ ] ส่ง transaction บน Anvil สำเร็จ

### ✅ Project Setup

- [ ] สร้างโครงสร้างโปรเจกต์ครบถ้วน
- [ ] มีไฟล์ `.env` ที่กำหนดค่าแล้ว
- [ ] มี `.gitignore` ที่ครบถ้วน
- [ ] เข้าใจ environment management

### ✅ Exercises

- [ ] ทำแบบฝึกหัดที่ 1-5 ครบทั้งหมด
- [ ] ทุก test ผ่าน
- [ ] Code ทำงานได้โดยไม่มี error

---

## 🎯 สรุป

ในบทนี้เราได้:

1. ✅ เรียนรู้พื้นฐาน blockchain และคำศัพท์สำคัญ
2. ✅ ติดตั้ง tools ทั้งหมด (Docker, Node.js, Python, Foundry)
3. ✅ Setup Anvil local node สำหรับ development
4. ✅ ทดสอบ RPC calls และส่ง transactions
5. ✅ สร้างโครงสร้างโปรเจกต์
6. ✅ เข้าใจการจัดการ environment variables
7. ✅ Setup Prometheus & Grafana เบื้องต้น

### 📚 บทต่อไป

**PART02 - Blockchain Nodes & RPC**
- Setup Geth node แบบละเอียด
- Archive node configuration
- RPC methods และการใช้งาน
- WebSocket subscriptions
- Node monitoring

---

## 🔗 Resources

### Official Documentation
- [Ethereum Documentation](https://ethereum.org/developers)
- [Foundry Book](https://book.getfoundry.sh/)
- [Web3.py Documentation](https://web3py.readthedocs.io/)
- [Docker Documentation](https://docs.docker.com/)

### Useful Tools
- [Etherscan](https://etherscan.io/) - Main net explorer
- [Sepolia Explorer](https://sepolia.etherscan.io/) - Test net explorer
- [Ethereum JSON-RPC Specification](https://ethereum.github.io/execution-apis/api-documentation/)

### Community
- [Ethereum Stack Exchange](https://ethereum.stackexchange.com/)
- [Foundry Telegram](https://t.me/foundry_rs)
- [/r/ethdev](https://reddit.com/r/ethdev)

---

**หมายเหตุ Production:**

เมื่อพัฒนาเสร็จและต้องการ deploy ไป production:

1. **Node Selection**
   - ใช้ Geth archive node แทน Anvil
   - หรือใช้ third-party RPC (Alchemy, Infura, QuickNode)
   - ตั้งค่า failover สำหรับ high availability

2. **Environment**
   - ใช้ strong passwords สำหรับ databases
   - เปิด SSL/TLS สำหรับทุก connections
   - Setup proper backup strategy

3. **Monitoring**
   - ตั้งค่า alerts สำหรับ critical metrics
   - Monitor node sync status
   - Track indexer lag

4. **Security**
   - Never commit `.env` files
   - Use secret management (Vault, AWS Secrets Manager)
   - Implement rate limiting
   - Enable authentication

---

**🎉 ยินดีด้วย! คุณผ่าน PART01 แล้ว!**

พร้อมสำหรับ [PART02 - Blockchain Nodes & RPC](./PART02.md) →

---

*Last Updated: 2025-11-06*
*Version: 1.0.0*
