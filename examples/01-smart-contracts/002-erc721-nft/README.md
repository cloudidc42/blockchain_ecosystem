# 002. ERC-721 NFT Collection

> NFT Collection พร้อม minting, metadata, royalty, และ reveal - ใช้งานได้จริง 100% ✅

## 📋 คำอธิบาย

ERC-721 NFT Collection แบบครบวงจร พร้อมฟีเจอร์สำหรับการสร้าง NFT project จริง

## 🎯 เทคโนโลยี

- **Solidity**: 0.8.20
- **Framework**: Foundry
- **Standard**: ERC-721, EIP-2981
- **Storage**: IPFS (for metadata)

## 📊 ระดับ

🟡 **Intermediate**

## 💡 ฟีเจอร์

### ERC-721 Standard
- ✅ Minting (single & batch)
- ✅ Transfer & Safe Transfer
- ✅ Approve & setApprovalForAll
- ✅ tokenURI with metadata

### NFT Features
- ✅ **Whitelist minting** - Pre-sale for selected addresses
- ✅ **Reveal mechanism** - Hide metadata before reveal
- ✅ **Royalty (EIP-2981)** - 2.5% default royalty
- ✅ **Pausable** - Emergency stop
- ✅ **Owner mint** - Free mint for team
- ✅ **Max supply** - Limited collection

## 🚀 การใช้งาน

### 1. Compile

```bash
forge build
```

### 2. Run Tests

```bash
forge test

# With gas report
forge test --gas-report

# With coverage
forge coverage
```

**Expected Output:**
```
Running 25 tests...
[PASS] testConstructor()
[PASS] testMint()
[PASS] testMintBatch()
[PASS] testReveal()
[PASS] testWhitelistMinting()
[PASS] testRoyaltyInfo()
...
Test result: ok. 25 passed; 0 failed
```

### 3. Deploy

```bash
# Local (Anvil)
forge script script/Deploy.s.sol:DeployNFTCollection \
  --rpc-url http://localhost:8545 \
  --private-key 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80 \
  --broadcast

# Testnet (Sepolia)
forge script script/Deploy.s.sol:DeployNFTCollection \
  --rpc-url $SEPOLIA_RPC_URL \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --verify
```

### 4. Interact

```bash
# Mint NFT
cast send $NFT_ADDRESS "mint()" \
  --value 0.08ether \
  --private-key $PRIVATE_KEY

# Check owner
cast call $NFT_ADDRESS "ownerOf(uint256)" 1

# Reveal collection
cast send $NFT_ADDRESS "reveal(string)" "ipfs://revealed/" \
  --private-key $OWNER_KEY
```

## 📖 Code Structure

```
002-erc721-nft/
├── src/
│   └── NFTCollection.sol        # 387 lines - Full ERC-721 implementation
├── test/
│   └── NFTCollection.t.sol      # 342 lines - 25+ test cases
├── script/
│   └── Deploy.s.sol             # Deployment script
├── foundry.toml
├── .env.example
└── README.md
```

## 🧪 การทดสอบ

### Test Coverage

| Category | Tests | Coverage |
|----------|-------|----------|
| Constructor | ✅ | 100% |
| Minting | ✅ | 100% |
| Transfers | ✅ | 100% |
| Approvals | ✅ | 100% |
| URI/Reveal | ✅ | 100% |
| Whitelist | ✅ | 100% |
| Pause | ✅ | 100% |
| Royalty | ✅ | 100% |
| Admin | ✅ | 100% |

### Test Scenarios

```solidity
// Minting
testMint()
testMintBatch()
testMintInsufficientPayment()
testMintMaxSupply()
testOwnerMint()

// Transfers
testTransferFrom()
testApprove()
testSetApprovalForAll()

// Reveal
testTokenURIUnrevealed()
testReveal()

// Whitelist
testWhitelistMinting()
testRemoveFromWhitelist()

// Royalty
testRoyaltyInfo()
testSetRoyalty()

// Admin
testPause()
testWithdraw()
testTransferOwnership()
```

## 🔒 Security Features

- ✅ **Access Control** - onlyOwner for admin functions
- ✅ **Pausable** - Emergency stop mechanism
- ✅ **Reentrancy Safe** - No external calls in critical functions
- ✅ **Zero Address Checks** - Prevent invalid transfers
- ✅ **Max Supply** - Hard limit on minting
- ✅ **Whitelist** - Controlled minting

## 📊 Gas Report

| Function | Gas Used |
|----------|----------|
| mint() | ~85,000 |
| mintBatch(5) | ~380,000 |
| transferFrom() | ~58,000 |
| reveal() | ~45,000 |

## 💰 Royalty (EIP-2981)

```solidity
// Default: 2.5% royalty
royaltyBasisPoints = 250; // 10000 = 100%

// Example: 1 ETH sale = 0.025 ETH royalty
(address receiver, uint256 royaltyAmount) = nft.royaltyInfo(tokenId, 1 ether);
// receiver = owner
// royaltyAmount = 0.025 ether
```

## ✅ Pass Criteria

1. ✅ Compile สำเร็จ ไม่มี errors
2. ✅ Tests ผ่านทั้งหมด (25/25)
3. ✅ Deploy สำเร็จและได้ contract address
4. ✅ Mint NFT ได้สำเร็จ
5. ✅ Transfer NFT ได้
6. ✅ Reveal mechanism ทำงานถูกต้อง
7. ✅ Royalty คำนวณถูกต้อง

## 🎓 สิ่งที่จะได้เรียนรู้

- ✅ ERC-721 standard implementation
- ✅ NFT minting mechanics
- ✅ Metadata & IPFS integration
- ✅ Reveal mechanism
- ✅ Whitelist pattern
- ✅ EIP-2981 Royalty standard
- ✅ Gas optimization for NFTs

## 🚀 Next Steps

หลังจากเรียนรู้โปรเจคนี้แล้ว ลองดู:

- **001-basic-erc20**: ERC-20 Token basics
- **003-erc1155-multi**: Multi-token standard
- **009-nft-marketplace**: NFT Marketplace

---

**License**: MIT
**Author**: Blockchain Explorer Examples
**Version**: 1.0.0
