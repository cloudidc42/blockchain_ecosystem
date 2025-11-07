# 🚀 100 Blockchain Explorer Examples - ใช้งานได้จริง 100%

> **ตัวอย่างโค้ดครบถ้วน 100 โปรเจค** สำหรับการสร้าง Blockchain Explorer และ Ecosystem ที่เกี่ยวข้อง

## 📋 สารบัญ

- [01. Smart Contracts (15 โปรเจค)](#01-smart-contracts)
- [02. Blockchain Interaction (15 โปรเจค)](#02-blockchain-interaction)
- [03. Backend/API (15 โปรเจค)](#03-backend-api)
- [04. Frontend/UI (15 โปรเจค)](#04-frontend-ui)
- [05. Data Analytics (10 โปรเจค)](#05-data-analytics)
- [06. DevOps/Infrastructure (10 โปรเจค)](#06-devops-infrastructure)
- [07. Security (10 โปรเจค)](#07-security)
- [08. Testing (5 โปรเจค)](#08-testing)
- [09. Utilities/Tools (5 โปรเจค)](#09-utilities-tools)

**รวมทั้งหมด: 100 โปรเจค** ✅

---

## 01. Smart Contracts

> 15 โปรเจค - สัญญาอัจฉริยะที่ใช้งานได้จริง พร้อม tests และ deployment scripts

### 001. Basic ERC-20 Token
- **คำอธิบาย**: Token ERC-20 พื้นฐานพร้อม mint, burn, pause
- **เทคโนโลยี**: Solidity 0.8.20, Foundry
- **ระดับ**: 🟢 Beginner
- **ไฟล์**: `01-smart-contracts/001-basic-erc20/`
- **ฟีเจอร์**:
  - ✅ Transfer, approve, transferFrom
  - ✅ Mint และ burn functions
  - ✅ Pausable mechanism
  - ✅ Access control (Ownable)
  - ✅ Unit tests ครบ 100%

### 002. ERC-721 NFT Collection
- **คำอธิบาย**: NFT Collection พร้อม metadata และ royalty
- **เทคโนโลยี**: Solidity 0.8.20, Foundry, IPFS
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `01-smart-contracts/002-erc721-nft/`
- **ฟีเจอร์**:
  - ✅ Minting NFTs พร้อม metadata URI
  - ✅ EIP-2981 Royalty standard
  - ✅ Enumerable extension
  - ✅ Reveal mechanism
  - ✅ Whitelist minting

### 003. ERC-1155 Multi-Token
- **คำอธิบาย**: Multi-token standard สำหรับ gaming/metaverse
- **เทคโนโลยี**: Solidity 0.8.20, Foundry
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `01-smart-contracts/003-erc1155-multi/`
- **ฟีเจอร์**:
  - ✅ Batch minting/transfer
  - ✅ Multiple token types
  - ✅ URI per token type
  - ✅ Supply tracking
  - ✅ Burnable tokens

### 004. DEX AMM (Automated Market Maker)
- **คำอธิบาย**: Uniswap V2-style DEX พร้อม liquidity pools
- **เทคโนโลยี**: Solidity 0.8.20, Foundry
- **ระดับ**: 🔴 Advanced
- **ไฟล์**: `01-smart-contracts/004-dex-amm/`
- **ฟีเจอร์**:
  - ✅ Constant product formula (x*y=k)
  - ✅ Add/remove liquidity
  - ✅ Swap tokens
  - ✅ LP token minting
  - ✅ Fee mechanism (0.3%)

### 005. Staking Contract
- **คำอธิบาย**: Token staking พร้อม rewards distribution
- **เทคโนโลยี**: Solidity 0.8.20, Foundry
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `01-smart-contracts/005-staking/`
- **ฟีเจอร์**:
  - ✅ Stake/unstake tokens
  - ✅ Reward calculation
  - ✅ Lock period
  - ✅ Emergency withdraw
  - ✅ Multiple reward rates

### 006. DAO Governance
- **คำอธิบาย**: DAO พร้อม proposal voting system
- **เทคโนโลยี**: Solidity 0.8.20, Foundry
- **ระดับ**: 🔴 Advanced
- **ไฟล์**: `01-smart-contracts/006-dao-governance/`
- **ฟีเจอร์**:
  - ✅ Create proposals
  - ✅ Vote (yes/no/abstain)
  - ✅ Quorum requirement
  - ✅ Timelock execution
  - ✅ Delegation

### 007. Multisig Wallet
- **คำอธิบาย**: Multi-signature wallet สำหรับการจัดการเงินร่วมกัน
- **เทคโนโลยี**: Solidity 0.8.20, Foundry
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `01-smart-contracts/007-multisig-wallet/`
- **ฟีเจอร์**:
  - ✅ M-of-N signature requirement
  - ✅ Submit/approve/execute transactions
  - ✅ Owner management
  - ✅ ETH และ ERC-20 support
  - ✅ Revoke confirmation

### 008. Vesting Contract
- **คำอธิบาย**: Token vesting สำหรับ team/investors
- **เทคโนโลยี**: Solidity 0.8.20, Foundry
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `01-smart-contracts/008-vesting/`
- **ฟีเจอร์**:
  - ✅ Linear vesting schedule
  - ✅ Cliff period
  - ✅ Multiple beneficiaries
  - ✅ Revocable vesting
  - ✅ Release tracking

### 009. NFT Marketplace
- **คำอธิบาย**: Marketplace สำหรับซื้อขาย NFTs
- **เทคโนโลยี**: Solidity 0.8.20, Foundry
- **ระดับ**: 🔴 Advanced
- **ไฟล์**: `01-smart-contracts/009-nft-marketplace/`
- **ฟีเจอร์**:
  - ✅ List NFT for sale
  - ✅ Buy NFT
  - ✅ Make offer
  - ✅ Accept/reject offer
  - ✅ Marketplace fee (2.5%)
  - ✅ Royalty support

### 010. Lending Protocol
- **คำอธิบาย**: Simple lending/borrowing protocol
- **เทคโนโลยี**: Solidity 0.8.20, Foundry
- **ระดับ**: 🔴 Advanced
- **ไฟล์**: `01-smart-contracts/010-lending/`
- **ฟีเจอร์**:
  - ✅ Supply/withdraw assets
  - ✅ Borrow/repay
  - ✅ Collateral management
  - ✅ Interest rate calculation
  - ✅ Liquidation mechanism

### 011. Oracle Price Feed
- **คำอธิบาย**: Decentralized oracle สำหรับ price feeds
- **เทคโนโลยี**: Solidity 0.8.20, Foundry
- **ระดับ**: 🔴 Advanced
- **ไฟล์**: `01-smart-contracts/011-oracle/`
- **ฟีเจอร์**:
  - ✅ Multiple oracle providers
  - ✅ Price aggregation (median)
  - ✅ Staleness check
  - ✅ Deviation threshold
  - ✅ Emergency pause

### 012. Token Bridge
- **คำอธิบาย**: Cross-chain bridge สำหรับ tokens
- **เทคโนโลยี**: Solidity 0.8.20, Foundry
- **ระดับ**: 🔴 Advanced
- **ไฟล์**: `01-smart-contracts/012-bridge/`
- **ฟีเจอร์**:
  - ✅ Lock/unlock mechanism
  - ✅ Mint/burn on destination
  - ✅ Relayer network
  - ✅ Merkle proof verification
  - ✅ Fee structure

### 013. Subscription Contract
- **คำอธิบาย**: Recurring payment subscription
- **เทคโนโลยี**: Solidity 0.8.20, Foundry
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `01-smart-contracts/013-subscription/`
- **ฟีเจอร์**:
  - ✅ Monthly/yearly plans
  - ✅ Auto-renewal
  - ✅ Cancel subscription
  - ✅ Grace period
  - ✅ Refund mechanism

### 014. Airdrop Contract
- **คำอธิบาย**: Merkle tree airdrop สำหรับ token distribution
- **เทคโนโลยี**: Solidity 0.8.20, Foundry
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `01-smart-contracts/014-airdrop/`
- **ฟีเจอร์**:
  - ✅ Merkle proof verification
  - ✅ Claim tracking
  - ✅ Multiple claim windows
  - ✅ Emergency withdraw
  - ✅ Gas-efficient claiming

### 015. Lottery/Raffle Contract
- **คำอธิบาย**: Provably fair lottery system
- **เทคโนโลยี**: Solidity 0.8.20, Foundry, Chainlink VRF
- **ระดับ**: 🔴 Advanced
- **ไฟล์**: `01-smart-contracts/015-lottery/`
- **ฟีเจอร์**:
  - ✅ Enter lottery
  - ✅ Chainlink VRF random number
  - ✅ Winner selection
  - ✅ Prize distribution
  - ✅ Round management

---

## 02. Blockchain Interaction

> 15 โปรเจค - การเชื่อมต่อและ interact กับ blockchain ผ่าน libraries ต่างๆ

### 016. Web3.py Basic Connection
- **คำอธิบาย**: เชื่อมต่อกับ Ethereum node ด้วย Web3.py
- **เทคโนโลยี**: Python 3.11, Web3.py
- **ระดับ**: 🟢 Beginner
- **ไฟล์**: `02-blockchain-interaction/016-web3py-basic/`
- **ฟีเจอร์**:
  - ✅ Connect to node (HTTP/WebSocket/IPC)
  - ✅ Get block information
  - ✅ Get transaction details
  - ✅ Check address balance
  - ✅ Listen to new blocks

### 017. Send ETH Transaction
- **คำอธิบาย**: ส่ง ETH transaction พร้อม gas estimation
- **เทคโนโลยี**: Python 3.11, Web3.py
- **ระดับ**: 🟢 Beginner
- **ไฟล์**: `02-blockchain-interaction/017-send-eth/`
- **ฟีเจอร์**:
  - ✅ Create transaction
  - ✅ Sign with private key
  - ✅ Estimate gas
  - ✅ Send transaction
  - ✅ Wait for confirmation

### 018. ERC-20 Token Interaction
- **คำอธิบาย**: อ่าน/เขียนข้อมูล ERC-20 tokens
- **เทคโนโลยี**: Python 3.11, Web3.py
- **ระดับ**: 🟢 Beginner
- **ไฟล์**: `02-blockchain-interaction/018-erc20-interact/`
- **ฟีเจอร์**:
  - ✅ Get token balance
  - ✅ Get token metadata
  - ✅ Transfer tokens
  - ✅ Approve spending
  - ✅ Check allowance

### 019. Smart Contract Deployment
- **คำอธิบาย**: Deploy smart contract ด้วย Web3.py
- **เทคโนโลยี**: Python 3.11, Web3.py
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `02-blockchain-interaction/019-contract-deploy/`
- **ฟีเจอร์**:
  - ✅ Compile Solidity
  - ✅ Deploy contract
  - ✅ Get contract address
  - ✅ Verify deployment
  - ✅ Constructor arguments

### 020. Event Listener
- **คำอธิบาย**: ฟัง events จาก smart contracts
- **เทคโนโลยี**: Python 3.11, Web3.py
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `02-blockchain-interaction/020-event-listener/`
- **ฟีเจอร์**:
  - ✅ Listen to Transfer events
  - ✅ Filter events by topics
  - ✅ Process event logs
  - ✅ WebSocket subscription
  - ✅ Event database storage

### 021. Batch RPC Requests
- **คำอธิบาย**: ส่ง RPC requests แบบ batch เพื่อประสิทธิภาพ
- **เทคโนโลยี**: Python 3.11, Web3.py, asyncio
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `02-blockchain-interaction/021-batch-rpc/`
- **ฟีเจอร์**:
  - ✅ Batch multiple calls
  - ✅ Async processing
  - ✅ Error handling
  - ✅ Rate limiting
  - ✅ Performance comparison

### 022. ENS Name Resolution
- **คำอธิบาย**: Resolve ENS names to addresses และ reverse
- **เทคโนโลยี**: Python 3.11, Web3.py, ENS
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `02-blockchain-interaction/022-ens-resolver/`
- **ฟีเจอร์**:
  - ✅ Name to address
  - ✅ Address to name
  - ✅ Get text records
  - ✅ Get avatar
  - ✅ Subdomains

### 023. Ethers.js Transaction Builder
- **คำอธิบาย**: Build และ send transactions ด้วย ethers.js
- **เทคโนโลยี**: JavaScript/TypeScript, ethers.js
- **ระดับ**: 🟢 Beginner
- **ไฟล์**: `02-blockchain-interaction/023-ethers-tx/`
- **ฟีเจอร์**:
  - ✅ Create wallet
  - ✅ Build transaction
  - ✅ EIP-1559 support
  - ✅ Sign and send
  - ✅ Receipt parsing

### 024. Contract Read/Write with Ethers
- **คำอธิบาย**: Read/write smart contract data ด้วย ethers.js
- **เทคโนโลยี**: TypeScript, ethers.js
- **ระดับ**: 🟢 Beginner
- **ไฟล์**: `02-blockchain-interaction/024-ethers-contract/`
- **ฟีเจอร์**:
  - ✅ Contract instance
  - ✅ Call view functions
  - ✅ Send transactions
  - ✅ Event filtering
  - ✅ TypeScript types

### 025. Wallet Connect Integration
- **คำอธิบาย**: เชื่อมต่อกับ wallet ผ่าน WalletConnect
- **เทคโนโลยี**: TypeScript, WalletConnect v2
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `02-blockchain-interaction/025-walletconnect/`
- **ฟีเจอร์**:
  - ✅ QR code connection
  - ✅ Sign messages
  - ✅ Send transactions
  - ✅ Switch chains
  - ✅ Disconnect

### 026. MetaMask Integration
- **คำอธิบาย**: เชื่อมต่อกับ MetaMask browser extension
- **เทคโนโลยี**: TypeScript, ethers.js
- **ระดับ**: 🟢 Beginner
- **ไฟล์**: `02-blockchain-interaction/026-metamask/`
- **ฟีเจอร์**:
  - ✅ Detect MetaMask
  - ✅ Connect wallet
  - ✅ Get account
  - ✅ Sign messages
  - ✅ Add network

### 027. Multi-chain Support
- **คำอธิบาย**: Support หลาย chains (Ethereum, Polygon, BSC, etc.)
- **เทคโนโลยี**: TypeScript, ethers.js, Viem
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `02-blockchain-interaction/027-multichain/`
- **ฟีเจอร์**:
  - ✅ Chain configuration
  - ✅ Auto-detect chain
  - ✅ Switch chains
  - ✅ Chain-specific logic
  - ✅ Provider management

### 028. Transaction Decoder
- **คำอธิบาย**: Decode transaction input data
- **เทคโนโลยี**: Python 3.11, Web3.py
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `02-blockchain-interaction/028-tx-decoder/`
- **ฟีเจอร์**:
  - ✅ Parse function signature
  - ✅ Decode parameters
  - ✅ ABI matching
  - ✅ Event log parsing
  - ✅ Human-readable output

### 029. Gas Price Tracker
- **คำอธิบาย**: Track และ predict gas prices
- **เทคโนโลยี**: Python 3.11, Web3.py
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `02-blockchain-interaction/029-gas-tracker/`
- **ฟีเจอร์**:
  - ✅ Current gas price
  - ✅ Historical data
  - ✅ EIP-1559 base fee
  - ✅ Priority fee suggestions
  - ✅ Gas price alerts

### 030. Block Explorer CLI
- **คำอธิบาย**: Command-line block explorer
- **เทคโนโลยี**: Python 3.11, Web3.py, Click
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `02-blockchain-interaction/030-explorer-cli/`
- **ฟีเจอร์**:
  - ✅ Get block by number/hash
  - ✅ Get transaction details
  - ✅ Get address info
  - ✅ Search functionality
  - ✅ Colored output

---

## 03. Backend/API

> 15 โปรเจค - REST API และ backend services สำหรับ blockchain data

### 031. FastAPI Block API
- **คำอธิบาย**: REST API สำหรับ block information
- **เทคโนโลยี**: FastAPI, SQLAlchemy, PostgreSQL
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `03-backend-api/031-block-api/`
- **ฟีเจอร์**:
  - ✅ GET /blocks (pagination)
  - ✅ GET /blocks/{number}
  - ✅ GET /blocks/latest
  - ✅ Caching with Redis
  - ✅ OpenAPI docs

### 032. Transaction API
- **คำอธิบาย**: REST API สำหรับ transactions
- **เทคโนโลยี**: FastAPI, SQLAlchemy, PostgreSQL
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `03-backend-api/032-transaction-api/`
- **ฟีเจอร์**:
  - ✅ GET /transactions/{hash}
  - ✅ GET /transactions (filters)
  - ✅ GET /address/{address}/transactions
  - ✅ Pagination
  - ✅ Response caching

### 033. Address API
- **คำอธิบาย**: REST API สำหรับ address information
- **เทคโนโลยี**: FastAPI, SQLAlchemy, PostgreSQL
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `03-backend-api/033-address-api/`
- **ฟีเจอร์**:
  - ✅ GET /address/{address}
  - ✅ Balance และ nonce
  - ✅ Transaction history
  - ✅ Token holdings
  - ✅ Contract detection

### 034. Token API
- **คำอธิบาย**: REST API สำหรับ ERC-20/721/1155 tokens
- **เทคโนโลยี**: FastAPI, SQLAlchemy, PostgreSQL
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `03-backend-api/034-token-api/`
- **ฟีเจอร์**:
  - ✅ GET /tokens (list all)
  - ✅ GET /tokens/{address}
  - ✅ Token holders
  - ✅ Transfer history
  - ✅ Price information

### 035. Search API
- **คำอธิบาย**: Universal search API (blocks, txs, addresses)
- **เทคโนโลยี**: FastAPI, Elasticsearch
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `03-backend-api/035-search-api/`
- **ฟีเจอร์**:
  - ✅ POST /search
  - ✅ Auto-detect query type
  - ✅ Fuzzy matching
  - ✅ Search suggestions
  - ✅ Full-text search

### 036. Stats API
- **คำอธิบาย**: Network statistics และ metrics
- **เทคโนโลยี**: FastAPI, ClickHouse
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `03-backend-api/036-stats-api/`
- **ฟีเจอร์**:
  - ✅ GET /stats/network
  - ✅ Transaction volume
  - ✅ Gas statistics
  - ✅ Active addresses
  - ✅ Time-series data

### 037. WebSocket API
- **คำอธิบาย**: Real-time data streaming via WebSocket
- **เทคโนโลยี**: FastAPI, WebSocket, Redis Pub/Sub
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `03-backend-api/037-websocket-api/`
- **ฟีเจอร์**:
  - ✅ Subscribe to new blocks
  - ✅ Subscribe to pending txs
  - ✅ Subscribe to address activity
  - ✅ Room management
  - ✅ Connection pooling

### 038. GraphQL API
- **คำอธิบาย**: GraphQL endpoint สำหรับ flexible queries
- **เทคโนโลยี**: Strawberry GraphQL, FastAPI
- **ระดับ**: 🔴 Advanced
- **ไฟล์**: `03-backend-api/038-graphql-api/`
- **ฟีเจอร์**:
  - ✅ Query blocks, txs, addresses
  - ✅ Nested queries
  - ✅ Mutations
  - ✅ Subscriptions
  - ✅ DataLoader for batching

### 039. Rate Limiting Middleware
- **คำอธิบาย**: Advanced rate limiting strategies
- **เทคโนโลยี**: FastAPI, Redis, Token Bucket
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `03-backend-api/039-rate-limiting/`
- **ฟีเจอร์**:
  - ✅ Token bucket algorithm
  - ✅ Per-IP limiting
  - ✅ Per-API-key limiting
  - ✅ Custom limits per endpoint
  - ✅ Rate limit headers

### 040. API Authentication
- **คำอธิบาย**: JWT authentication และ authorization
- **เทคโนโลยี**: FastAPI, JWT, bcrypt
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `03-backend-api/040-auth/`
- **ฟีเจอร์**:
  - ✅ User registration
  - ✅ Login/logout
  - ✅ JWT tokens
  - ✅ Refresh tokens
  - ✅ Role-based access

### 041. Caching Strategy
- **คำอธิบาย**: Multi-layer caching implementation
- **เทคโนโลยี**: FastAPI, Redis, Memcached
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `03-backend-api/041-caching/`
- **ฟีเจอร์**:
  - ✅ Response caching
  - ✅ Query result caching
  - ✅ Cache invalidation
  - ✅ TTL strategies
  - ✅ Cache-aside pattern

### 042. API Versioning
- **คำอธิบาย**: API version management (v1, v2, etc.)
- **เทคโนโลยี**: FastAPI
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `03-backend-api/042-versioning/`
- **ฟีเจอร์**:
  - ✅ URL path versioning
  - ✅ Header versioning
  - ✅ Deprecation warnings
  - ✅ Version migration
  - ✅ Documentation per version

### 043. Error Handling
- **คำอธิบาย**: Centralized error handling และ logging
- **เทคโนโลยี**: FastAPI, Sentry
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `03-backend-api/043-error-handling/`
- **ฟีเจอร์**:
  - ✅ Custom exception handlers
  - ✅ Error response format
  - ✅ Sentry integration
  - ✅ Error tracking
  - ✅ Retry logic

### 044. Background Tasks
- **คำอธิบาย**: Async background jobs with Celery
- **เทคโนโลยี**: Celery, Redis, FastAPI
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `03-backend-api/044-background-tasks/`
- **ฟีเจอร์**:
  - ✅ Task queue
  - ✅ Periodic tasks
  - ✅ Task monitoring
  - ✅ Result backend
  - ✅ Retry mechanism

### 045. API Documentation
- **คำอธิบาย**: Auto-generated API docs with examples
- **เทคโนโลยี**: FastAPI, Swagger UI, ReDoc
- **ระดับ**: 🟢 Beginner
- **ไฟล์**: `03-backend-api/045-documentation/`
- **ฟีเจอร์**:
  - ✅ OpenAPI schema
  - ✅ Interactive Swagger UI
  - ✅ ReDoc documentation
  - ✅ Example requests/responses
  - ✅ Code generation

---

## 04. Frontend/UI

> 15 โปรเจค - User interfaces สำหรับ blockchain explorer

### 046. Block List Page
- **คำอธิบาย**: แสดงรายการ blocks แบบ real-time
- **เทคโนโลยี**: Next.js 14, React 18, TailwindCSS
- **ระดับ**: 🟢 Beginner
- **ไฟล์**: `04-frontend-ui/046-block-list/`
- **ฟีเจอร์**:
  - ✅ Paginated block list
  - ✅ Real-time updates
  - ✅ Sort by number/time
  - ✅ Block summary cards
  - ✅ Loading states

### 047. Block Detail Page
- **คำอธิบาย**: แสดงรายละเอียด block
- **เทคโนโลยี**: Next.js 14, React 18, shadcn/ui
- **ระดับ**: 🟢 Beginner
- **ไฟล์**: `04-frontend-ui/047-block-detail/`
- **ฟีเจอร์**:
  - ✅ Block information
  - ✅ Transaction list
  - ✅ Gas usage chart
  - ✅ Copy buttons
  - ✅ Navigation (prev/next)

### 048. Transaction List
- **คำอธิบาย**: แสดงรายการ transactions พร้อม filters
- **เทคโนโลยี**: Next.js 14, React 18, TailwindCSS
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `04-frontend-ui/048-transaction-list/`
- **ฟีเจอร์**:
  - ✅ Filter by status/type
  - ✅ Search by hash
  - ✅ Pagination
  - ✅ Transaction cards
  - ✅ Value formatting

### 049. Transaction Detail
- **คำอธิบาย**: แสดงรายละเอียด transaction
- **เทคโนโลยี**: Next.js 14, React 18, shadcn/ui
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `04-frontend-ui/049-transaction-detail/`
- **ฟีเจอร์**:
  - ✅ Transaction info
  - ✅ Input data decoder
  - ✅ Event logs
  - ✅ Internal transactions
  - ✅ State changes

### 050. Address Page
- **คำอธิบาย**: Address overview และ analytics
- **เทคโนโลยี**: Next.js 14, React 18, Recharts
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `04-frontend-ui/050-address-page/`
- **ฟีเจอร์**:
  - ✅ Balance display
  - ✅ Transaction history
  - ✅ Token holdings
  - ✅ Activity chart
  - ✅ QR code

### 051. Token Page
- **คำอธิบาย**: Token information และ holders
- **เทคโนโลยี**: Next.js 14, React 18, TailwindCSS
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `04-frontend-ui/051-token-page/`
- **ฟีเจอร์**:
  - ✅ Token metadata
  - ✅ Holder list
  - ✅ Transfer history
  - ✅ Supply chart
  - ✅ Contract info

### 052. Search Component
- **คำอธิบาย**: Universal search bar with autocomplete
- **เทคโนโลยี**: React 18, TypeScript
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `04-frontend-ui/052-search/`
- **ฟีเจอร์**:
  - ✅ Autocomplete suggestions
  - ✅ Recent searches
  - ✅ Keyboard navigation
  - ✅ Search history
  - ✅ Mobile responsive

### 053. Dashboard Page
- **คำอธิบาย**: Network overview dashboard
- **เทคโนโลยี**: Next.js 14, Recharts, shadcn/ui
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `04-frontend-ui/053-dashboard/`
- **ฟีเจอร์**:
  - ✅ Network stats cards
  - ✅ Transaction volume chart
  - ✅ Gas price chart
  - ✅ Latest blocks/txs
  - ✅ Active addresses

### 054. Dark Mode Toggle
- **คำอธิบาย**: Theme switcher with persistence
- **เทคโนโลยี**: Next.js 14, next-themes
- **ระดับ**: 🟢 Beginner
- **ไฟล์**: `04-frontend-ui/054-dark-mode/`
- **ฟีเจอร์**:
  - ✅ Light/dark/system modes
  - ✅ LocalStorage persistence
  - ✅ Smooth transitions
  - ✅ CSS variables
  - ✅ No flash of unstyled content

### 055. Wallet Connect Button
- **คำอธิบาย**: Connect wallet component
- **เทคโนโลยี**: React 18, ethers.js, wagmi
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `04-frontend-ui/055-wallet-connect/`
- **ฟีเจอร์**:
  - ✅ Multiple wallet support
  - ✅ Account display
  - ✅ Chain switcher
  - ✅ Disconnect button
  - ✅ Connection status

### 056. Chart Components
- **คำอธิบาย**: Reusable chart library
- **เทคโนโลยี**: React 18, Recharts, D3.js
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `04-frontend-ui/056-charts/`
- **ฟีเจอร์**:
  - ✅ Line chart
  - ✅ Bar chart
  - ✅ Area chart
  - ✅ Pie chart
  - ✅ Responsive design

### 057. Table Component
- **คำอธิบาย**: Advanced data table with sorting/filtering
- **เทคโนโลยี**: React 18, TanStack Table
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `04-frontend-ui/057-table/`
- **ฟีเจอร์**:
  - ✅ Column sorting
  - ✅ Column filtering
  - ✅ Pagination
  - ✅ Row selection
  - ✅ Virtual scrolling

### 058. Notification System
- **คำอธิบาย**: Toast notifications และ alerts
- **เทคโนโลยี**: React 18, react-hot-toast
- **ระดับ**: 🟢 Beginner
- **ไฟล์**: `04-frontend-ui/058-notifications/`
- **ฟีเจอร์**:
  - ✅ Success/error/info toasts
  - ✅ Custom positions
  - ✅ Auto-dismiss
  - ✅ Action buttons
  - ✅ Stacking

### 059. Loading States
- **คำอธิบาย**: Skeleton loaders และ spinners
- **เทคโนโลยี**: React 18, TailwindCSS
- **ระดับ**: 🟢 Beginner
- **ไฟล์**: `04-frontend-ui/059-loading-states/`
- **ฟีเจอร์**:
  - ✅ Skeleton screens
  - ✅ Spinner components
  - ✅ Progress bars
  - ✅ Shimmer effect
  - ✅ Suspense boundaries

### 060. Mobile Responsive Layout
- **คำอธิบาย**: Responsive design patterns
- **เทคโนโลยี**: Next.js 14, TailwindCSS
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `04-frontend-ui/060-responsive/`
- **ฟีเจอร์**:
  - ✅ Mobile-first design
  - ✅ Breakpoint system
  - ✅ Hamburger menu
  - ✅ Touch gestures
  - ✅ PWA support

---

## 05. Data Analytics

> 10 โปรเจค - Data analysis และ visualization

### 061. Daily Transaction Stats
- **คำอธิบาย**: วิเคราะห์ transaction volume รายวัน
- **เทคโนโลยี**: Python 3.11, ClickHouse, Pandas
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `05-data-analytics/061-daily-stats/`
- **ฟีเจอร์**:
  - ✅ Daily transaction count
  - ✅ Daily transaction volume (ETH)
  - ✅ Average gas price
  - ✅ Active addresses
  - ✅ CSV/JSON export

### 062. Gas Price Analysis
- **คำอธิบาย**: วิเคราะห์ gas price patterns
- **เทคโนโลยี**: Python 3.11, ClickHouse, Matplotlib
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `05-data-analytics/062-gas-analysis/`
- **ฟีเจอร์**:
  - ✅ Hourly gas statistics
  - ✅ Peak hours detection
  - ✅ Price predictions
  - ✅ Visualization charts
  - ✅ Anomaly detection

### 063. Token Analytics
- **คำอธิบาย**: ERC-20 token metrics และ analytics
- **เทคโนโลยี**: Python 3.11, ClickHouse, Pandas
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `05-data-analytics/063-token-analytics/`
- **ฟีเจอร์**:
  - ✅ Holder distribution
  - ✅ Transfer velocity
  - ✅ Supply analysis
  - ✅ Top holders
  - ✅ Price correlation

### 064. Address Behavior Analysis
- **คำอธิบาย**: วิเคราะห์พฤติกรรม addresses
- **เทคโนโลยี**: Python 3.11, ClickHouse, Scikit-learn
- **ระดับ**: 🔴 Advanced
- **ไฟล์**: `05-data-analytics/064-address-behavior/`
- **ฟีเจอร์**:
  - ✅ Activity patterns
  - ✅ Whale detection
  - ✅ Bot identification
  - ✅ Clustering analysis
  - ✅ Risk scoring

### 065. Network Health Dashboard
- **คำอธิบาย**: Dashboard สำหรับ network metrics
- **เทคโนโลยี**: Python 3.11, Streamlit, ClickHouse
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `05-data-analytics/065-network-health/`
- **ฟีเจอร์**:
  - ✅ Real-time metrics
  - ✅ Historical trends
  - ✅ Interactive charts
  - ✅ Alert system
  - ✅ Export reports

### 066. Smart Contract Analytics
- **คำอธิบาย**: วิเคราะห์การใช้งาน smart contracts
- **เทคโนโลยี**: Python 3.11, ClickHouse
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `05-data-analytics/066-contract-analytics/`
- **ฟีเจอร์**:
  - ✅ Function call frequency
  - ✅ Gas consumption
  - ✅ Error rate analysis
  - ✅ Popular contracts
  - ✅ Upgrade tracking

### 067. DEX Trading Analytics
- **คำอธิบาย**: วิเคราะห์ DEX trading activity
- **เทคโนโลยี**: Python 3.11, ClickHouse, Pandas
- **ระดับ**: 🔴 Advanced
- **ไฟล์**: `05-data-analytics/067-dex-analytics/`
- **ฟีเจอร์**:
  - ✅ Trading volume
  - ✅ Price impact
  - ✅ Liquidity analysis
  - ✅ Swap paths
  - ✅ Arbitrage detection

### 068. NFT Market Analytics
- **คำอธิบาย**: วิเคราะห์ NFT marketplace data
- **เทคโนโลยี**: Python 3.11, ClickHouse, Pandas
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `05-data-analytics/068-nft-analytics/`
- **ฟีเจอร์**:
  - ✅ Sales volume
  - ✅ Floor price tracking
  - ✅ Rarity analysis
  - ✅ Wash trading detection
  - ✅ Collection rankings

### 069. Time-series Forecasting
- **คำอธิบาย**: Predict network metrics with ML
- **เทคโนโลยี**: Python 3.11, Prophet, TensorFlow
- **ระดับ**: 🔴 Advanced
- **ไฟล์**: `05-data-analytics/069-forecasting/`
- **ฟีเจอร์**:
  - ✅ Transaction volume prediction
  - ✅ Gas price forecasting
  - ✅ Trend analysis
  - ✅ Seasonality detection
  - ✅ Model evaluation

### 070. Report Generator
- **คำอธิบาย**: สร้าง PDF reports อัตโนมัติ
- **เทคโนโลยี**: Python 3.11, ReportLab, Jinja2
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `05-data-analytics/070-report-generator/`
- **ฟีเจอร์**:
  - ✅ Daily/weekly/monthly reports
  - ✅ Charts และ tables
  - ✅ PDF export
  - ✅ Email delivery
  - ✅ Custom templates

---

## 06. DevOps/Infrastructure

> 10 โปรเจค - Deployment และ infrastructure automation

### 071. Docker Multi-stage Build
- **คำอธิบาย**: Optimized Docker images สำหรับ production
- **เทคโนโลยี**: Docker, Alpine Linux
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `06-devops-infrastructure/071-docker-multistage/`
- **ฟีเจอร์**:
  - ✅ Multi-stage builds
  - ✅ Layer caching
  - ✅ Minimal image size
  - ✅ Security best practices
  - ✅ Health checks

### 072. Docker Compose Stack
- **คำอธิบาย**: Complete stack orchestration
- **เทคโนโลยี**: Docker Compose
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `06-devops-infrastructure/072-docker-compose/`
- **ฟีเจอร์**:
  - ✅ Multi-service setup
  - ✅ Networks และ volumes
  - ✅ Environment configs
  - ✅ Service dependencies
  - ✅ Development/production profiles

### 073. Kubernetes Deployment
- **คำอธิบาย**: K8s manifests สำหรับ production
- **เทคโนโลยี**: Kubernetes, Helm
- **ระดับ**: 🔴 Advanced
- **ไฟล์**: `06-devops-infrastructure/073-k8s-deployment/`
- **ฟีเจอร์**:
  - ✅ Deployments
  - ✅ Services (ClusterIP, LoadBalancer)
  - ✅ Ingress
  - ✅ ConfigMaps และ Secrets
  - ✅ Horizontal Pod Autoscaler

### 074. Helm Charts
- **คำอธิบาย**: Helm charts สำหรับ easy deployment
- **เทคโนโลยี**: Helm 3, Kubernetes
- **ระดับ**: 🔴 Advanced
- **ไฟล์**: `06-devops-infrastructure/074-helm-charts/`
- **ฟีเจอร์**:
  - ✅ Parameterized templates
  - ✅ Values files (dev/staging/prod)
  - ✅ Dependencies
  - ✅ Hooks
  - ✅ Testing

### 075. CI/CD Pipeline
- **คำอธิบาย**: GitHub Actions workflow
- **เทคโนโลยี**: GitHub Actions, Docker
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `06-devops-infrastructure/075-cicd-pipeline/`
- **ฟีเจอร์**:
  - ✅ Automated testing
  - ✅ Build และ push images
  - ✅ Deploy to staging/prod
  - ✅ Rollback mechanism
  - ✅ Slack notifications

### 076. Terraform AWS Infrastructure
- **คำอธิบาย**: Infrastructure as Code สำหรับ AWS
- **เทคโนโลยี**: Terraform, AWS
- **ระดับ**: 🔴 Advanced
- **ไฟล์**: `06-devops-infrastructure/076-terraform-aws/`
- **ฟีเจอร์**:
  - ✅ VPC และ subnets
  - ✅ ECS/EKS cluster
  - ✅ RDS databases
  - ✅ Load balancers
  - ✅ S3 และ CloudFront

### 077. Prometheus Monitoring
- **คำอธิบาย**: Metrics collection setup
- **เทคโนโลยี**: Prometheus, Node Exporter
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `06-devops-infrastructure/077-prometheus/`
- **ฟีเจอร์**:
  - ✅ Prometheus config
  - ✅ Service discovery
  - ✅ Recording rules
  - ✅ Alert rules
  - ✅ Exporters setup

### 078. Grafana Dashboards
- **คำอธิบาย**: Pre-configured monitoring dashboards
- **เทคโนโลยี**: Grafana, JSON
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `06-devops-infrastructure/078-grafana-dashboards/`
- **ฟีเจอร์**:
  - ✅ System metrics dashboard
  - ✅ Application metrics dashboard
  - ✅ Blockchain metrics dashboard
  - ✅ Alerts visualization
  - ✅ Template variables

### 079. Logging with ELK Stack
- **คำอธิบาย**: Centralized logging solution
- **เทคโนโลยี**: Elasticsearch, Logstash, Kibana
- **ระดับ**: 🔴 Advanced
- **ไฟล์**: `06-devops-infrastructure/079-elk-logging/`
- **ฟีเจอร์**:
  - ✅ Log aggregation
  - ✅ Parsing และ filtering
  - ✅ Index management
  - ✅ Kibana dashboards
  - ✅ Search queries

### 080. Backup and Restore
- **คำอธิบาย**: Automated backup strategies
- **เทคโนโลยี**: Bash, Cron, S3
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `06-devops-infrastructure/080-backup-restore/`
- **ฟีเจอร์**:
  - ✅ Database backups (PostgreSQL, ClickHouse)
  - ✅ Incremental backups
  - ✅ S3 storage
  - ✅ Restore scripts
  - ✅ Backup verification

---

## 07. Security

> 10 โปรเจค - Security best practices และ tools

### 081. API Key Management
- **คำอธิบาย**: Secure API key generation และ storage
- **เทคโนโลยี**: Python 3.11, cryptography, Redis
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `07-security/081-api-key-mgmt/`
- **ฟีเจอร์**:
  - ✅ Secure key generation
  - ✅ Hashed storage
  - ✅ Key rotation
  - ✅ Usage tracking
  - ✅ Revocation

### 082. Input Validation
- **คำอธิบาย**: Comprehensive input validation
- **เทคโนโลยี**: Python 3.11, Pydantic
- **ระดับ**: 🟢 Beginner
- **ไฟล์**: `07-security/082-input-validation/`
- **ฟีเจอร์**:
  - ✅ Address validation
  - ✅ Hash validation
  - ✅ Number validation
  - ✅ XSS prevention
  - ✅ SQL injection prevention

### 083. Rate Limiting
- **คำอธิบาย**: Token bucket rate limiter
- **เทคโนโลยี**: Python 3.11, Redis
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `07-security/083-rate-limiting/`
- **ฟีเจอร์**:
  - ✅ Token bucket algorithm
  - ✅ Distributed rate limiting
  - ✅ Per-user limits
  - ✅ Burst handling
  - ✅ Rate limit headers

### 084. SSL/TLS Configuration
- **คำอธิบาย**: HTTPS setup with Let's Encrypt
- **เทคโนโลยี**: Nginx, Certbot
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `07-security/084-ssl-tls/`
- **ฟีเจอร์**:
  - ✅ SSL certificate generation
  - ✅ Auto-renewal
  - ✅ HSTS headers
  - ✅ TLS 1.3
  - ✅ A+ SSL Labs rating

### 085. Secrets Management
- **คำอธิบาย**: Secure secrets storage with Vault
- **เทคโนโลยี**: HashiCorp Vault, Docker
- **ระดับ**: 🔴 Advanced
- **ไฟล์**: `07-security/085-secrets-mgmt/`
- **ฟีเจอร์**:
  - ✅ Vault setup
  - ✅ Secret storage
  - ✅ Dynamic secrets
  - ✅ Encryption as a service
  - ✅ Audit logging

### 086. SQL Injection Prevention
- **คำอธิบาย**: Prepared statements และ ORM usage
- **เทคโนโลยี**: Python 3.11, SQLAlchemy
- **ระดับ**: 🟢 Beginner
- **ไฟล์**: `07-security/086-sql-injection/`
- **ฟีเจอร์**:
  - ✅ Parameterized queries
  - ✅ ORM best practices
  - ✅ Input sanitization
  - ✅ Detection examples
  - ✅ Testing

### 087. CORS Configuration
- **คำอธิบาย**: Secure CORS setup
- **เทคโนโลยี**: FastAPI, Python
- **ระดับ**: 🟢 Beginner
- **ไฟล์**: `07-security/087-cors/`
- **ฟีเจอร์**:
  - ✅ Origin whitelisting
  - ✅ Credentials handling
  - ✅ Preflight requests
  - ✅ Header configuration
  - ✅ Testing

### 088. DDoS Protection
- **คำอธิบาย**: DDoS mitigation strategies
- **เทคโนโลยี**: Nginx, iptables, Cloudflare
- **ระดับ**: 🔴 Advanced
- **ไฟล์**: `07-security/088-ddos-protection/`
- **ฟีเจอร์**:
  - ✅ Connection limits
  - ✅ Request rate limiting
  - ✅ IP blacklisting
  - ✅ Challenge pages
  - ✅ Traffic analysis

### 089. Audit Logging
- **คำอธิบาย**: Comprehensive audit trail
- **เทคโนโลยี**: Python 3.11, PostgreSQL
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `07-security/089-audit-logging/`
- **ฟีเจอร์**:
  - ✅ Action logging
  - ✅ User tracking
  - ✅ IP logging
  - ✅ Tamper-proof logs
  - ✅ Log analysis

### 090. Smart Contract Security Audit
- **คำอธิบาย**: Security checklist และ tools
- **เทคโนโลยี**: Slither, Mythril, Foundry
- **ระดับ**: 🔴 Advanced
- **ไฟล์**: `07-security/090-contract-audit/`
- **ฟีเจอร์**:
  - ✅ Static analysis
  - ✅ Vulnerability detection
  - ✅ Gas optimization
  - ✅ Best practices checklist
  - ✅ Report generation

---

## 08. Testing

> 5 โปรเจค - Testing strategies และ frameworks

### 091. Unit Testing (Python)
- **คำอธิบาย**: Comprehensive unit tests with pytest
- **เทคโนโลยี**: pytest, pytest-cov, pytest-mock
- **ระดับ**: 🟢 Beginner
- **ไฟล์**: `08-testing/091-unit-testing-python/`
- **ฟีเจอร์**:
  - ✅ Test fixtures
  - ✅ Parametrized tests
  - ✅ Mocking
  - ✅ Coverage reporting
  - ✅ CI integration

### 092. Integration Testing
- **คำอธิบาย**: API integration tests
- **เทคโนโลยี**: pytest, httpx, TestClient
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `08-testing/092-integration-testing/`
- **ฟีเจอร์**:
  - ✅ API endpoint tests
  - ✅ Database integration
  - ✅ Test database setup
  - ✅ Transaction rollback
  - ✅ Fixtures

### 093. Smart Contract Testing
- **คำอธิบาย**: Foundry test suite
- **เทคโนโลยี**: Foundry, Solidity
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `08-testing/093-contract-testing/`
- **ฟีเจอร์**:
  - ✅ Unit tests
  - ✅ Fuzz testing
  - ✅ Invariant testing
  - ✅ Gas reporting
  - ✅ Coverage

### 094. E2E Testing
- **คำอธิบาย**: End-to-end tests with Playwright
- **เทคโนโลยี**: Playwright, TypeScript
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `08-testing/094-e2e-testing/`
- **ฟีเจอร์**:
  - ✅ Browser automation
  - ✅ Page object model
  - ✅ Screenshots
  - ✅ Video recording
  - ✅ Parallel execution

### 095. Load Testing
- **คำอธิบาย**: Performance testing with k6
- **เทคโนโลยี**: k6, Grafana
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `08-testing/095-load-testing/`
- **ฟีเจอร์**:
  - ✅ Load scenarios
  - ✅ Stress testing
  - ✅ Spike testing
  - ✅ Metrics collection
  - ✅ Threshold alerts

---

## 09. Utilities/Tools

> 5 โปรเจค - Command-line tools และ utilities

### 096. CLI Block Explorer
- **คำอธิบาย**: Full-featured CLI explorer
- **เทคโนโลยี**: Python 3.11, Click, Rich
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `09-utilities/096-cli-explorer/`
- **ฟีเจอร์**:
  - ✅ Block/tx/address lookup
  - ✅ Colored output
  - ✅ Tables และ charts
  - ✅ Config file support
  - ✅ History

### 097. Address Generator
- **คำอธิบาย**: Vanity address generator
- **เทคโนโลยี**: Python 3.11, eth-account
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `09-utilities/097-address-generator/`
- **ฟีเจอร์**:
  - ✅ Vanity patterns
  - ✅ Multi-threaded generation
  - ✅ Progress bar
  - ✅ Secure key storage
  - ✅ Benchmarking

### 098. Gas Price Monitor
- **คำอธิบาย**: Real-time gas price tracking
- **เทคโนโลยี**: Python 3.11, Web3.py
- **ระดับ**: 🟢 Beginner
- **ไฟล์**: `09-utilities/098-gas-monitor/`
- **ฟีเจอร์**:
  - ✅ Real-time updates
  - ✅ Desktop notifications
  - ✅ Price alerts
  - ✅ Historical chart
  - ✅ Terminal UI

### 099. Data Export Tool
- **คำอธิบาย**: Export blockchain data to CSV/JSON
- **เทคโนโลยี**: Python 3.11, Pandas
- **ระดับ**: 🟡 Intermediate
- **ไฟล์**: `09-utilities/099-data-export/`
- **ฟีเจอร์**:
  - ✅ Batch export
  - ✅ Multiple formats
  - ✅ Filter options
  - ✅ Progress tracking
  - ✅ Compression

### 100. Blockchain Snapshot Tool
- **คำอธิบาย**: Create/restore blockchain snapshots
- **เทคโนโลยี**: Python 3.11, geth/anvil
- **ระดับ**: 🔴 Advanced
- **ไฟล์**: `09-utilities/100-snapshot-tool/`
- **ฟีเจอร์**:
  - ✅ Create snapshots
  - ✅ Restore from snapshot
  - ✅ Incremental backups
  - ✅ Compression
  - ✅ Verification

---

## 🎯 การใช้งาน

### Requirements

- **Node.js**: 18+ (สำหรับ frontend/JS examples)
- **Python**: 3.11+ (สำหรับ backend/Python examples)
- **Foundry**: Latest (สำหรับ smart contracts)
- **Docker**: 20+ (สำหรับ containerized examples)

### Installation

```bash
# Clone repository
git clone https://github.com/your-repo/blockchain_ecosystem.git
cd blockchain_ecosystem/examples

# เลือกโปรเจคที่ต้องการ
cd 01-smart-contracts/001-basic-erc20

# ติดตั้ง dependencies และรัน
# (แต่ละโปรเจคมี README.md พร้อมคำแนะนำ)
```

### โครงสร้างโปรเจค

แต่ละโปรเจคมีโครงสร้างดังนี้:

```
xxx-project-name/
├── README.md           # คำแนะนำการใช้งาน
├── src/                # Source code
├── tests/              # Test files
├── .env.example        # Environment template
└── package.json        # Dependencies (ถ้ามี)
    หรือ
    requirements.txt    # Python dependencies (ถ้ามี)
```

## 📊 Statistics

| หมวดหมู่ | จำนวน | ระดับ Beginner | ระดับ Intermediate | ระดับ Advanced |
|---------|-------|----------------|-------------------|----------------|
| Smart Contracts | 15 | 1 | 7 | 7 |
| Blockchain Interaction | 15 | 5 | 9 | 1 |
| Backend/API | 15 | 1 | 13 | 1 |
| Frontend/UI | 15 | 5 | 10 | 0 |
| Data Analytics | 10 | 0 | 7 | 3 |
| DevOps/Infrastructure | 10 | 0 | 6 | 4 |
| Security | 10 | 3 | 4 | 3 |
| Testing | 5 | 1 | 4 | 0 |
| Utilities/Tools | 5 | 1 | 3 | 1 |
| **รวม** | **100** | **17** | **63** | **20** |

## 🏆 Learning Path

แนะนำเส้นทางการเรียนรู้:

### Level 1: Beginner (17 โปรเจค)
เริ่มต้นที่ 🟢 Beginner projects เพื่อเข้าใจพื้นฐาน

### Level 2: Intermediate (63 โปรเจค)
ต่อด้วย 🟡 Intermediate projects เพื่อเพิ่มทักษะ

### Level 3: Advanced (20 โปรเจค)
ท้าทายตัวเองด้วย 🔴 Advanced projects

## 📝 License

MIT License - ใช้งานได้อย่างอิสระ

## 🤝 Contributing

Pull requests are welcome! โปรดอ่าน CONTRIBUTING.md ก่อน contribute

---

**หมายเหตุ**: ทุกโปรเจคทดสอบแล้วและใช้งานได้จริง 100% ✅

สร้างโดย: Blockchain Explorer Documentation Team
อัพเดทล่าสุด: 2025-11-07
