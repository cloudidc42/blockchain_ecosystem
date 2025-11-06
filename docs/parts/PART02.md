# PART 02 - Blockchain Nodes & RPC

> คู่มือสมบูรณ์สำหรับการตั้งค่า Blockchain Nodes และการใช้งาน RPC Methods

**เป้าหมายของบทนี้:**
- เข้าใจ Ethereum node types และความแตกต่าง
- ติดตั้งและตั้งค่า Geth archive node
- เรียนรู้ RPC methods ทั้งหมด
- ใช้งาน WebSocket subscriptions
- Monitor node performance
- Optimize node configuration

**ระยะเวลา:** 5-8 ชั่วโมง
**ระดับ:** Intermediate

---

## 📑 สารบัญ

1. [Ethereum Node Types](#1-ethereum-node-types)
2. [Geth Installation](#2-geth-installation)
3. [Geth Configuration](#3-geth-configuration)
4. [Archive Node Setup](#4-archive-node-setup)
5. [RPC Methods Overview](#5-rpc-methods-overview)
6. [Core RPC Methods](#6-core-rpc-methods)
7. [Block & Transaction Methods](#7-block--transaction-methods)
8. [State & Storage Methods](#8-state--storage-methods)
9. [WebSocket Subscriptions](#9-websocket-subscriptions)
10. [Node Monitoring](#10-node-monitoring)
11. [Performance Optimization](#11-performance-optimization)
12. [Troubleshooting](#12-troubleshooting)
13. [แบบฝึกหัด](#13-แบบฝึกหัด)
14. [เกณฑ์ผ่าน](#14-เกณฑ์ผ่าน)

---

## 1. Ethereum Node Types

### 1.1 Full Node

```
📊 Full Node Characteristics

┌─────────────────────────────────────────────────────────┐
│                      FULL NODE                          │
├─────────────────────────────────────────────────────────┤
│ Storage:                                                │
│  ✅ All block headers                                   │
│  ✅ All block bodies (transactions)                     │
│  ✅ Current state (latest)                              │
│  ❌ Historical states                                    │
│                                                         │
│ Capabilities:                                           │
│  ✅ Validate all blocks                                 │
│  ✅ Query recent data                                   │
│  ❌ Query historical state                              │
│                                                         │
│ Requirements:                                           │
│  💾 Disk: ~500-800 GB                                   │
│  ⏱️ Sync Time: 1-3 days                                 │
│  💰 Cost: Medium                                         │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Archive Node

```
📊 Archive Node Characteristics

┌─────────────────────────────────────────────────────────┐
│                    ARCHIVE NODE                         │
├─────────────────────────────────────────────────────────┤
│ Storage:                                                │
│  ✅ All block headers                                   │
│  ✅ All block bodies (transactions)                     │
│  ✅ Current state                                       │
│  ✅ ALL historical states                               │
│                                                         │
│ Capabilities:                                           │
│  ✅ Validate all blocks                                 │
│  ✅ Query any data at any block                         │
│  ✅ eth_call at historical blocks                       │
│  ✅ Full blockchain analysis                            │
│                                                         │
│ Requirements:                                           │
│  💾 Disk: 12-15 TB (growing ~50GB/month)               │
│  ⏱️ Sync Time: 2-4 weeks                                │
│  💰 Cost: High                                           │
│                                                         │
│ ⚠️ Required for Block Explorers!                       │
└─────────────────────────────────────────────────────────┘
```

### 1.3 Light Node

```
📊 Light Node Characteristics

┌─────────────────────────────────────────────────────────┐
│                     LIGHT NODE                          │
├─────────────────────────────────────────────────────────┤
│ Storage:                                                │
│  ✅ Block headers only                                  │
│  ❌ Block bodies                                         │
│  ❌ State                                                │
│                                                         │
│ Capabilities:                                           │
│  ✅ Verify block headers                                │
│  ❌ Full validation                                      │
│  ⚠️ Relies on full nodes                                │
│                                                         │
│ Requirements:                                           │
│  💾 Disk: ~400 MB                                       │
│  ⏱️ Sync Time: Minutes                                  │
│  💰 Cost: Very Low                                       │
└─────────────────────────────────────────────────────────┘
```

### 1.4 Node Type Comparison

| Feature | Light | Full | Archive |
|---------|-------|------|---------|
| **Disk Space** | ~400 MB | ~600 GB | ~12 TB |
| **Sync Time** | Minutes | 1-3 days | 2-4 weeks |
| **Can Validate** | Headers | All | All |
| **Historical Queries** | ❌ | Limited | ✅ Full |
| **Explorer Suitable** | ❌ | Partial | ✅ Best |
| **Cost/Month** | $5-10 | $50-100 | $200-500 |

---

## 2. Geth Installation

### 2.1 Install on Linux (Ubuntu/Debian)

```bash
# Method 1: From PPA (Recommended)
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install -y ethereum

# Verify
geth version

# Method 2: Download Binary
wget https://gethstore.blob.core.windows.net/builds/geth-linux-amd64-1.13.5-916d6a44.tar.gz
tar -xzf geth-linux-amd64-1.13.5-916d6a44.tar.gz
sudo mv geth-linux-amd64-1.13.5-916d6a44/geth /usr/local/bin/
geth version
```

### 2.2 Install on macOS

```bash
# Using Homebrew
brew tap ethereum/ethereum
brew install ethereum

# Verify
geth version
```

### 2.3 Install on Windows

```powershell
# Using Chocolatey
choco install geth

# Or download from:
# https://geth.ethereum.org/downloads/

# Verify
geth version
```

### 2.4 Docker Installation

```bash
# Pull official image
docker pull ethereum/client-go:latest

# Run Geth in Docker
docker run -d \
  --name geth-node \
  -v /path/to/datadir:/root/.ethereum \
  -p 8545:8545 \
  -p 8546:8546 \
  -p 30303:30303 \
  ethereum/client-go:latest \
  --http \
  --http.addr 0.0.0.0 \
  --http.api eth,net,web3 \
  --syncmode snap

# Check logs
docker logs -f geth-node
```

---

## 3. Geth Configuration

### 3.1 Basic Geth Configuration

```bash
# Start Geth with basic settings
geth \
  --mainnet \
  --datadir ./geth-data \
  --http \
  --http.addr 0.0.0.0 \
  --http.port 8545 \
  --http.api eth,net,web3 \
  --http.corsdomain "*" \
  --ws \
  --ws.addr 0.0.0.0 \
  --ws.port 8546 \
  --ws.api eth,net,web3 \
  --syncmode snap
```

### 3.2 Configuration File (config.toml)

```toml
# Geth Configuration File
# Save as: geth-config.toml

[Eth]
NetworkId = 1
SyncMode = "snap"
DatabaseCache = 4096
TrieTimeout = 3600000000000
EnablePreimageRecording = false

[Eth.TxPool]
Locals = []
NoLocals = false
Journal = "transactions.rlp"
Rejournal = 3600000000000
PriceLimit = 1
PriceBump = 10
AccountSlots = 16
GlobalSlots = 5120
AccountQueue = 64
GlobalQueue = 1024
Lifetime = 10800000000000

[Node]
DataDir = "./geth-data"
IPCPath = "geth.ipc"
HTTPHost = "0.0.0.0"
HTTPPort = 8545
HTTPVirtualHosts = ["*"]
HTTPModules = ["eth", "net", "web3", "txpool"]
WSHost = "0.0.0.0"
WSPort = 8546
WSModules = ["eth", "net", "web3"]
GraphQLVirtualHosts = ["localhost"]

[Node.P2P]
MaxPeers = 50
NoDiscovery = false
BootstrapNodes = []
StaticNodes = []
TrustedNodes = []
ListenAddr = ":30303"
EnableMsgEvents = false

[Node.HTTPTimeouts]
ReadTimeout = 30000000000
WriteTimeout = 30000000000
IdleTimeout = 120000000000

[Metrics]
Enabled = true
HTTP = "0.0.0.0"
Port = 6060
```

### 3.3 Start with Configuration File

```bash
geth --config geth-config.toml
```

### 3.4 Important Flags Explained

```bash
# Sync Modes
--syncmode snap     # Fast sync (recommended for full node)
--syncmode full     # Full validation (required for archive)

# Network
--mainnet          # Ethereum mainnet
--sepolia          # Sepolia testnet
--goerli           # Goerli testnet (deprecated)

# Data Directory
--datadir <path>   # Where to store blockchain data

# HTTP RPC
--http                    # Enable HTTP-RPC server
--http.addr 0.0.0.0      # Listen on all interfaces
--http.port 8545         # HTTP-RPC port
--http.api <apis>        # APIs to expose
--http.corsdomain "*"    # CORS domains (use carefully!)

# WebSocket
--ws                # Enable WS-RPC server
--ws.addr 0.0.0.0   # WS listen address
--ws.port 8546      # WS port
--ws.api <apis>     # APIs to expose

# Performance
--cache <MB>        # Memory for internal caching
--maxpeers <num>    # Maximum peers

# Archive Mode
--gcmode archive    # Keep all historical state
--syncmode full     # Full sync (required with archive)
```

---

## 4. Archive Node Setup

### 4.1 Hardware Requirements

```
💻 Recommended Hardware for Archive Node

CPU:    8+ cores (16+ recommended)
RAM:    32 GB minimum (64 GB recommended)
Disk:   15 TB NVMe SSD (fast I/O critical!)
        - NOT HDD (too slow)
        - NOT SATA SSD (too slow)
        - NVMe PCIe 4.0 recommended
Network: 1 Gbps+ connection
        - Unlimited bandwidth or 5+ TB/month
```

### 4.2 Start Archive Node

```bash
# Create systemd service file
sudo tee /etc/systemd/system/geth-archive.service << 'EOF'
[Unit]
Description=Geth Archive Node
After=network.target

[Service]
Type=simple
User=ethereum
Group=ethereum
ExecStart=/usr/local/bin/geth \
  --mainnet \
  --datadir /mnt/nvme/geth-archive \
  --http \
  --http.addr 0.0.0.0 \
  --http.port 8545 \
  --http.api eth,net,web3,debug,trace,txpool \
  --http.corsdomain "*" \
  --http.vhosts "*" \
  --ws \
  --ws.addr 0.0.0.0 \
  --ws.port 8546 \
  --ws.api eth,net,web3,debug,trace \
  --ws.origins "*" \
  --syncmode full \
  --gcmode archive \
  --cache 16384 \
  --maxpeers 50 \
  --metrics \
  --metrics.addr 0.0.0.0 \
  --metrics.port 6060
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create user
sudo useradd -m -s /bin/bash ethereum

# Create data directory
sudo mkdir -p /mnt/nvme/geth-archive
sudo chown -R ethereum:ethereum /mnt/nvme/geth-archive

# Start service
sudo systemctl daemon-reload
sudo systemctl enable geth-archive
sudo systemctl start geth-archive

# Check status
sudo systemctl status geth-archive

# View logs
sudo journalctl -u geth-archive -f
```

### 4.3 Monitor Sync Progress

```bash
# Attach to Geth console
geth attach http://localhost:8545

# In console:
> eth.syncing
{
  currentBlock: 15000000,
  highestBlock: 18000000,
  knownStates: 950000000,
  pulledStates: 900000000,
  startingBlock: 0
}

# Calculate progress
> progress = (eth.syncing.currentBlock / eth.syncing.highestBlock) * 100
50

# Check if synced
> eth.syncing
false  // Returns false when fully synced

# Exit
> exit
```

### 4.4 Estimate Sync Time

```python
# Calculate estimated time
from datetime import datetime, timedelta

current_block = 15_000_000
highest_block = 18_000_000
blocks_per_hour = 50_000  # Typical speed for archive sync

remaining_blocks = highest_block - current_block
hours_remaining = remaining_blocks / blocks_per_hour
days_remaining = hours_remaining / 24

print(f"Estimated time remaining: {days_remaining:.1f} days")
# Output: Estimated time remaining: 2.5 days
```

---

## 5. RPC Methods Overview

### 5.1 RPC Categories

```
📚 Ethereum JSON-RPC Methods

┌─────────────────────────────────────────────────────┐
│                  WEB3 METHODS                       │
│  - web3_clientVersion                               │
│  - web3_sha3                                        │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                   NET METHODS                       │
│  - net_version                                      │
│  - net_listening                                    │
│  - net_peerCount                                    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                   ETH METHODS                       │
│  ├─ Block Methods                                   │
│  │   - eth_blockNumber                             │
│  │   - eth_getBlockByNumber                        │
│  │   - eth_getBlockByHash                          │
│  │                                                  │
│  ├─ Transaction Methods                            │
│  │   - eth_sendRawTransaction                      │
│  │   - eth_getTransactionByHash                    │
│  │   - eth_getTransactionReceipt                   │
│  │                                                  │
│  ├─ State Methods                                   │
│  │   - eth_getBalance                              │
│  │   - eth_getCode                                 │
│  │   - eth_getStorageAt                            │
│  │   - eth_call                                    │
│  │                                                  │
│  ├─ Gas Methods                                     │
│  │   - eth_gasPrice                                │
│  │   - eth_estimateGas                             │
│  │   - eth_feeHistory                              │
│  │                                                  │
│  └─ Filter/Log Methods                             │
│      - eth_getLogs                                  │
│      - eth_newFilter                                │
│      - eth_getFilterLogs                            │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                 DEBUG METHODS                       │
│  - debug_traceTransaction                           │
│  - debug_traceBlockByNumber                         │
│  - debug_storageRangeAt                             │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                 TRACE METHODS                       │
│  - trace_block                                      │
│  - trace_transaction                                │
│  - trace_filter                                     │
└─────────────────────────────────────────────────────┘
```

---

## 6. Core RPC Methods

### 6.1 web3_clientVersion

```bash
# Get client version
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"web3_clientVersion",
    "params":[],
    "id":1
  }'

# Response:
{
  "jsonrpc":"2.0",
  "id":1,
  "result":"Geth/v1.13.5-stable/linux-amd64/go1.21.4"
}
```

### 6.2 eth_chainId

```bash
# Get chain ID
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"eth_chainId",
    "params":[],
    "id":1
  }'

# Response:
{"jsonrpc":"2.0","id":1,"result":"0x1"}  # 1 = Mainnet
```

### 6.3 eth_blockNumber

```bash
# Get latest block number
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"eth_blockNumber",
    "params":[],
    "id":1
  }'

# Response:
{"jsonrpc":"2.0","id":1,"result":"0x112a880"}  # 18000000 in hex
```

### 6.4 eth_gasPrice

```bash
# Get current gas price
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"eth_gasPrice",
    "params":[],
    "id":1
  }'

# Response:
{"jsonrpc":"2.0","id":1,"result":"0x4a817c800"}  # 20 gwei
```

### 6.5 eth_getBalance

```bash
# Get account balance
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"eth_getBalance",
    "params":[
      "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
      "latest"
    ],
    "id":1
  }'

# Response:
{"jsonrpc":"2.0","id":1,"result":"0xde0b6b3a7640000"}  # 1 ETH in wei
```

---

## 7. Block & Transaction Methods

### 7.1 eth_getBlockByNumber

```bash
# Get block by number (with full transactions)
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"eth_getBlockByNumber",
    "params":["0x112a880", true],
    "id":1
  }'

# Response includes full block data with all transactions
```

```python
# Python example
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

# Get latest block
block = w3.eth.get_block('latest', full_transactions=True)

print(f"Block number: {block['number']}")
print(f"Block hash: {block['hash'].hex()}")
print(f"Miner: {block['miner']}")
print(f"Timestamp: {block['timestamp']}")
print(f"Gas used: {block['gasUsed']}")
print(f"Transactions: {len(block['transactions'])}")

# Iterate transactions
for tx in block['transactions']:
    print(f"  Tx: {tx['hash'].hex()}")
    print(f"    From: {tx['from']}")
    print(f"    To: {tx['to']}")
    print(f"    Value: {w3.from_wei(tx['value'], 'ether')} ETH")
```

### 7.2 eth_getTransactionByHash

```bash
# Get transaction details
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"eth_getTransactionByHash",
    "params":["0x1234..."],
    "id":1
  }'
```

```python
# Python example
tx = w3.eth.get_transaction('0x1234...')

print(f"Hash: {tx['hash'].hex()}")
print(f"From: {tx['from']}")
print(f"To: {tx['to']}")
print(f"Value: {w3.from_wei(tx['value'], 'ether')} ETH")
print(f"Gas: {tx['gas']}")
print(f"Gas Price: {w3.from_wei(tx['gasPrice'], 'gwei')} gwei")
print(f"Nonce: {tx['nonce']}")
print(f"Block: {tx['blockNumber']}")
```

### 7.3 eth_getTransactionReceipt

```bash
# Get transaction receipt
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"eth_getTransactionReceipt",
    "params":["0x1234..."],
    "id":1
  }'
```

```python
# Python example
receipt = w3.eth.get_transaction_receipt('0x1234...')

print(f"Status: {'Success' if receipt['status'] == 1 else 'Failed'}")
print(f"Gas Used: {receipt['gasUsed']}")
print(f"Effective Gas Price: {w3.from_wei(receipt['effectiveGasPrice'], 'gwei')} gwei")
print(f"Logs: {len(receipt['logs'])}")

# Parse logs
for log in receipt['logs']:
    print(f"  Log from: {log['address']}")
    print(f"    Topics: {[t.hex() for t in log['topics']]}")
    print(f"    Data: {log['data']}")
```

### 7.4 eth_getLogs

```bash
# Get logs by filter
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"eth_getLogs",
    "params":[{
      "fromBlock": "0x112a880",
      "toBlock": "latest",
      "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
      "topics": [
        "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
      ]
    }],
    "id":1
  }'
```

```python
# Python example - Get Transfer events
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

# ERC-20 Transfer event signature
transfer_signature = w3.keccak(text="Transfer(address,address,uint256)").hex()

# Filter parameters
filter_params = {
    'fromBlock': 18000000,
    'toBlock': 'latest',
    'address': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',  # USDC
    'topics': [transfer_signature]
}

# Get logs
logs = w3.eth.get_logs(filter_params)

print(f"Found {len(logs)} Transfer events")

for log in logs[:5]:  # First 5
    from_addr = "0x" + log['topics'][1].hex()[-40:]
    to_addr = "0x" + log['topics'][2].hex()[-40:]
    amount = int(log['data'], 16) / 10**6  # USDC has 6 decimals

    print(f"Transfer: {from_addr} → {to_addr}")
    print(f"  Amount: ${amount:,.2f}")
    print(f"  Block: {log['blockNumber']}")
    print(f"  Tx: {log['transactionHash'].hex()}")
    print()
```

---

## 8. State & Storage Methods

### 8.1 eth_call

```python
# Call contract method without sending transaction
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

# ERC-20 contract
usdc_address = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

# balanceOf(address) function signature
# Function selector: first 4 bytes of keccak256("balanceOf(address)")
function_selector = w3.keccak(text="balanceOf(address)")[:4].hex()
address_param = "000000000000000000000000742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
data = function_selector + address_param

# Call contract
result = w3.eth.call({
    'to': usdc_address,
    'data': data
}, 'latest')

# Decode result
balance = int(result.hex(), 16) / 10**6  # USDC has 6 decimals
print(f"Balance: ${balance:,.2f}")
```

### 8.2 eth_getCode

```python
# Get contract bytecode
code = w3.eth.get_code('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48')

if code == b'' or code == '0x':
    print("Not a contract (EOA)")
else:
    print(f"Contract bytecode: {code.hex()[:100]}...")
    print(f"Bytecode size: {len(code)} bytes")
```

### 8.3 eth_getStorageAt

```python
# Read contract storage slot
storage_slot = 0
storage_value = w3.eth.get_storage_at(
    '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    storage_slot,
    'latest'
)

print(f"Storage at slot {storage_slot}: {storage_value.hex()}")
```

---

## 9. WebSocket Subscriptions

### 9.1 Subscribe to New Blocks

```javascript
// Node.js example
const Web3 = require('web3');
const web3 = new Web3('ws://localhost:8546');

// Subscribe to new block headers
const subscription = web3.eth.subscribe('newBlockHeaders', (error, blockHeader) => {
    if (error) {
        console.error('Error:', error);
        return;
    }

    console.log('New block:',blockHeader.number);
    console.log('  Hash:', blockHeader.hash);
    console.log('  Miner:', blockHeader.miner);
    console.log('  Timestamp:', new Date(blockHeader.timestamp * 1000));
    console.log('  Gas Used:', blockHeader.gasUsed);
    console.log('  Transactions:', blockHeader.transactions.length);
});

// Unsubscribe after 1 hour
setTimeout(() => {
    subscription.unsubscribe((error, success) => {
        if (success) {
            console.log('Unsubscribed successfully');
        }
    });
}, 3600000);
```

### 9.2 Subscribe to Pending Transactions

```javascript
// Subscribe to pending transactions
const pendingTxSubscription = web3.eth.subscribe('pendingTransactions', (error, txHash) => {
    if (error) {
        console.error('Error:', error);
        return;
    }

    // Get transaction details
    web3.eth.getTransaction(txHash)
        .then(tx => {
            if (tx) {
                console.log('Pending tx:', tx.hash);
                console.log('  From:', tx.from);
                console.log('  To:', tx.to);
                console.log('  Value:', web3.utils.fromWei(tx.value, 'ether'), 'ETH');
                console.log('  Gas Price:', web3.utils.fromWei(tx.gasPrice, 'gwei'), 'gwei');
            }
        });
});
```

### 9.3 Subscribe to Logs

```javascript
// Subscribe to specific contract events
const logSubscription = web3.eth.subscribe('logs', {
    address: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',  // USDC
    topics: [
        web3.utils.sha3('Transfer(address,address,uint256)')
    ]
}, (error, log) => {
    if (error) {
        console.error('Error:', error);
        return;
    }

    console.log('Transfer event detected:');
    console.log('  Block:', log.blockNumber);
    console.log('  Tx:', log.transactionHash);
    console.log('  From:', '0x' + log.topics[1].slice(26));
    console.log('  To:', '0x' + log.topics[2].slice(26));
});
```

---

## 10. Node Monitoring

### 10.1 Geth Metrics

```bash
# Enable metrics
geth --metrics --metrics.addr 0.0.0.0 --metrics.port 6060

# Access metrics
curl http://localhost:6060/debug/metrics

# Prometheus format
curl http://localhost:6060/debug/metrics/prometheus
```

### 10.2 Key Metrics to Monitor

```python
# Python monitoring script
import requests
import time
from prometheus_client import start_http_server, Gauge

# Prometheus metrics
CHAIN_HEAD = Gauge('geth_chain_head', 'Current blockchain head')
PEER_COUNT = Gauge('geth_peer_count', 'Number of peers')
SYNC_PROGRESS = Gauge('geth_sync_progress', 'Sync progress percentage')
GAS_PRICE = Gauge('geth_gas_price', 'Current gas price in gwei')

def get_geth_metrics():
    rpc_url = 'http://localhost:8545'

    # Get block number
    response = requests.post(rpc_url, json={
        'jsonrpc': '2.0',
        'method': 'eth_blockNumber',
        'params': [],
        'id': 1
    })
    block_number = int(response.json()['result'], 16)
    CHAIN_HEAD.set(block_number)

    # Get peer count
    response = requests.post(rpc_url, json={
        'jsonrpc': '2.0',
        'method': 'net_peerCount',
        'params': [],
        'id': 1
    })
    peer_count = int(response.json()['result'], 16)
    PEER_COUNT.set(peer_count)

    # Get gas price
    response = requests.post(rpc_url, json={
        'jsonrpc': '2.0',
        'method': 'eth_gasPrice',
        'params': [],
        'id': 1
    })
    gas_price_wei = int(response.json()['result'], 16)
    gas_price_gwei = gas_price_wei / 10**9
    GAS_PRICE.set(gas_price_gwei)

    # Check sync status
    response = requests.post(rpc_url, json={
        'jsonrpc': '2.0',
        'method': 'eth_syncing',
        'params': [],
        'id': 1
    })
    sync_status = response.json()['result']

    if sync_status == False:
        SYNC_PROGRESS.set(100)
    else:
        current = int(sync_status['currentBlock'], 16)
        highest = int(sync_status['highestBlock'], 16)
        progress = (current / highest) * 100
        SYNC_PROGRESS.set(progress)

if __name__ == '__main__':
    # Start Prometheus metrics server
    start_http_server(9000)

    # Update metrics every 15 seconds
    while True:
        try:
            get_geth_metrics()
            time.sleep(15)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(15)
```

### 10.3 Health Check Script

```bash
#!/bin/bash
# geth-health-check.sh

RPC_URL="http://localhost:8545"

# Check if Geth is responding
if ! curl -s -X POST $RPC_URL \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"net_version","params":[],"id":1}' \
  > /dev/null; then
  echo "❌ Geth not responding"
  exit 1
fi

# Check sync status
SYNC_STATUS=$(curl -s -X POST $RPC_URL \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_syncing","params":[],"id":1}' \
  | jq -r '.result')

if [ "$SYNC_STATUS" = "false" ]; then
  echo "✅ Geth fully synced"
else
  CURRENT=$(echo $SYNC_STATUS | jq -r '.currentBlock' | xargs printf "%d")
  HIGHEST=$(echo $SYNC_STATUS | jq -r '.highestBlock' | xargs printf "%d")
  PROGRESS=$(echo "scale=2; ($CURRENT / $HIGHEST) * 100" | bc)
  echo "⏳ Syncing: $PROGRESS% ($CURRENT / $HIGHEST)"
fi

# Check peer count
PEER_COUNT=$(curl -s -X POST $RPC_URL \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"net_peerCount","params":[],"id":1}' \
  | jq -r '.result' | xargs printf "%d")

echo "👥 Peers: $PEER_COUNT"

if [ $PEER_COUNT -lt 5 ]; then
  echo "⚠️  Low peer count"
fi

# Check disk space
DISK_USAGE=$(df -h /mnt/nvme/geth-archive | awk 'NR==2 {print $5}' | sed 's/%//')
echo "💾 Disk usage: $DISK_USAGE%"

if [ $DISK_USAGE -gt 90 ]; then
  echo "⚠️  Disk space critical!"
  exit 1
fi

echo "✅ Health check passed"
```

---

## 11. Performance Optimization

### 11.1 Cache Optimization

```bash
# Increase cache for better performance
# Rule of thumb: Use 50-75% of available RAM

# For 32GB RAM:
--cache 16384

# For 64GB RAM:
--cache 32768

# For 128GB RAM:
--cache 65536
```

### 11.2 Connection Optimization

```bash
# Optimize peer connections
--maxpeers 100         # More peers = better sync
--nat extip:<your-ip>  # If behind NAT

# Limit connections if bandwidth limited
--maxpeers 25
```

### 11.3 Database Optimization

```bash
# Ancient data (older blocks) can be stored separately
--datadir.ancient /path/to/ancient

# Prune old state (for full node, not archive)
geth snapshot prune-state --datadir ./geth-data
```

---

## 12. Troubleshooting

### 12.1 Common Issues

#### Slow Sync

```bash
# Check disk I/O
iostat -x 1

# If disk is bottleneck, use faster SSD
# NVMe > SATA SSD > HDD

# Increase cache
--cache 32768

# More peers
--maxpeers 100
```

#### Peer Connection Issues

```bash
# Check if port is open
sudo ufw allow 30303/tcp
sudo ufw allow 30303/udp

# Manual peer addition
admin.addPeer("enode://pubkey@ip:port")
```

#### Out of Memory

```bash
# Reduce cache
--cache 4096

# Or add more RAM/swap

# Add swap (temporary solution)
sudo fallocate -l 32G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 12.2 Reset and Resync

```bash
# If corrupted, remove chaindata and resync
geth removedb --datadir ./geth-data

# Start fresh sync
geth --datadir ./geth-data ...
```

---

## 13. แบบฝึกหัด

### แบบฝึกหัดที่ 1: Install และ Start Geth

**เป้าหมาย:** ติดตั้ง Geth และ start node สำเร็จ

**ขั้นตอน:**
1. ติดตั้ง Geth บนระบบของคุณ
2. Start Geth บน Sepolia testnet
3. ตรวจสอบ sync status
4. ทดสอบ RPC calls

**เกณฑ์ผ่าน:**
- ✅ Geth start สำเร็จ
- ✅ เริ่ม sync ได้
- ✅ RPC responding

---

### แบบฝึกหัดที่ 2: RPC Method Testing

**เป้าหมาย:** ทดสอบ RPC methods ต่างๆ

สร้างไฟล์ `test_rpc.py`:

```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

# Test 1: Connection
assert w3.is_connected(), "Not connected"
print("✅ Connected to node")

# Test 2: Chain ID
chain_id = w3.eth.chain_id
print(f"✅ Chain ID: {chain_id}")
assert chain_id in [1, 11155111], "Invalid chain"  # Mainnet or Sepolia

# Test 3: Latest block
latest_block = w3.eth.block_number
print(f"✅ Latest block: {latest_block}")
assert latest_block > 0, "No blocks"

# Test 4: Gas price
gas_price = w3.eth.gas_price
gas_price_gwei = w3.from_wei(gas_price, 'gwei')
print(f"✅ Gas price: {gas_price_gwei} gwei")

# Test 5: Get block
block = w3.eth.get_block('latest')
print(f"✅ Block hash: {block['hash'].hex()}")
assert 'transactions' in block, "No transactions field"

# Test 6: Account balance
vitalik = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
balance = w3.eth.get_balance(vitalik)
balance_eth = w3.from_wei(balance, 'ether')
print(f"✅ Vitalik's balance: {balance_eth} ETH")

print("\n✅ All tests passed!")
```

รัน:
```bash
python test_rpc.py
```

---

### แบบฝึกหัดที่ 3: Block Explorer

**เป้าหมาย:** สร้าง simple block explorer CLI

```python
from web3 import Web3
from datetime import datetime

w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

def explore_block(block_number):
    block = w3.eth.get_block(block_number, full_transactions=True)

    print(f"\n{'='*60}")
    print(f"BLOCK #{block['number']}")
    print(f"{'='*60}")
    print(f"Hash:      {block['hash'].hex()}")
    print(f"Timestamp: {datetime.fromtimestamp(block['timestamp'])}")
    print(f"Miner:     {block['miner']}")
    print(f"Gas Used:  {block['gasUsed']:,} / {block['gasLimit']:,}")
    print(f"Txs:       {len(block['transactions'])}")

    print(f"\nTransactions:")
    print(f"{'-'*60}")

    for i, tx in enumerate(block['transactions'][:10], 1):  # First 10
        value_eth = w3.from_wei(tx['value'], 'ether')
        print(f"{i}. {tx['hash'].hex()[:10]}...")
        print(f"   {tx['from'][:10]}... → {tx['to'][:10] if tx['to'] else 'CONTRACT'}...")
        print(f"   {value_eth} ETH | Gas: {tx['gas']:,}")

    if len(block['transactions']) > 10:
        print(f"   ... and {len(block['transactions']) - 10} more")

# Explore latest block
latest = w3.eth.block_number
explore_block(latest)
```

---

## 14. เกณฑ์ผ่าน

### ✅ Knowledge Check

- [ ] เข้าใจความแตกต่างระหว่าง Full Node และ Archive Node
- [ ] รู้จัก RPC methods หลักๆ
- [ ] เข้าใจ WebSocket subscriptions
- [ ] รู้วิธี monitor node health

### ✅ Technical Skills

- [ ] ติดตั้ง Geth สำเร็จ
- [ ] Start และ config Geth ได้
- [ ] ใช้ RPC methods ได้
- [ ] เขียน script monitor node ได้

### ✅ Practical

- [ ] Node sync แล้ว (อย่างน้อย partial)
- [ ] ทดสอบ RPC calls สำเร็จ
- [ ] ทำแบบฝึกหัดครบ
- [ ] Code ทำงานได้

---

## 🎯 สรุป

ในบทนี้เราได้:

1. ✅ เรียนรู้ Ethereum node types
2. ✅ ติดตั้งและตั้งค่า Geth
3. ✅ Setup archive node สำหรับ explorer
4. ✅ เรียนรู้ RPC methods ทั้งหมด
5. ✅ ใช้งาน WebSocket subscriptions
6. ✅ Monitor node performance
7. ✅ Optimize และ troubleshoot

### 📚 บทต่อไป

**PART03 - Smart Contracts & Solidity**
- เขียน Smart Contracts
- Deploy และ interact
- Events และ logs
- Testing contracts

---

*Last Updated: 2025-11-06*
*Version: 1.0.0*
