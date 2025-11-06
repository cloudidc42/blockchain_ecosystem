# PART03 - Smart Contracts & Solidity

> **เนื้อหา**: Solidity Basics, ERC Standards (Full Implementation), Foundry Development, Contract Interaction
>
> **เป้าหมาย**: เข้าใจการพัฒนา Smart Contracts ด้วย Solidity และ Foundry framework พร้อม deploy และทดสอบ
>
> **ระยะเวลา**: 8-12 ชั่วโมง
>
> **Prerequisites**: PART01, PART02, Foundry installed

---

## 📑 สารบัญ

1. [Solidity Basics](#solidity-basics)
2. [ERC-20 Token Standard](#erc-20-token-standard)
3. [ERC-721 NFT Standard](#erc-721-nft-standard)
4. [ERC-1155 Multi-Token Standard](#erc-1155-multi-token-standard)
5. [Foundry Development](#foundry-development)
6. [Contract Interaction](#contract-interaction)
7. [แบบฝึกหัด](#แบบฝึกหัด)

---

## Solidity Basics

### 1.1 Solidity คืออะไร?

**Solidity** เป็นภาษาโปรแกรมมิ่งแบบ high-level ที่ออกแบบมาสำหรับการเขียน Smart Contracts บน Ethereum และ EVM-compatible blockchains

**ลักษณะสำคัญ**:
- **Statically typed**: ต้องประกาศ type ของตัวแปร
- **Object-oriented**: รองรับ inheritance, libraries, complex types
- **Compiled language**: compile เป็น EVM bytecode
- **Similar to JavaScript/C++**: syntax คล้ายคลึงกัน

### 1.2 โครงสร้างพื้นฐาน

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// Contract declaration
contract MyFirstContract {
    // State variables (stored on blockchain)
    uint256 public myNumber;
    address public owner;

    // Constructor (runs once on deployment)
    constructor() {
        owner = msg.sender;
        myNumber = 0;
    }

    // Function
    function setNumber(uint256 _newNumber) public {
        myNumber = _newNumber;
    }

    // View function (doesn't modify state)
    function getNumber() public view returns (uint256) {
        return myNumber;
    }
}
```

**อธิบายส่วนประกอบ**:

```
┌─────────────────────────────────────────┐
│  SPDX-License-Identifier: MIT           │ ← License declaration
├─────────────────────────────────────────┤
│  pragma solidity ^0.8.20;               │ ← Compiler version
├─────────────────────────────────────────┤
│  contract MyFirstContract {             │ ← Contract declaration
│    uint256 public myNumber;             │ ← State variable
│    address public owner;                │
│                                         │
│    constructor() { ... }                │ ← Initialization
│                                         │
│    function setNumber(...) { ... }      │ ← State-changing function
│    function getNumber(...) { ... }      │ ← View function
│  }                                      │
└─────────────────────────────────────────┘
```

### 1.3 Data Types

#### Value Types

```solidity
contract DataTypes {
    // Boolean
    bool public isActive = true;

    // Unsigned integers
    uint8 public smallNumber = 255;        // 0 to 255
    uint256 public largeNumber = 1000000;  // 0 to 2^256-1
    uint public defaultUint = 42;          // same as uint256

    // Signed integers
    int8 public temperature = -10;         // -128 to 127
    int256 public balance = -1000;         // -2^255 to 2^255-1

    // Address (20 bytes = 160 bits)
    address public myAddress = 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb8;
    address payable public recipient;      // can receive Ether

    // Bytes
    bytes1 public singleByte = 0xff;
    bytes32 public hash = keccak256("hello");

    // String
    string public name = "Blockchain Explorer";

    // Enum
    enum Status { Pending, Active, Inactive }
    Status public currentStatus = Status.Active;
}
```

#### Reference Types

```solidity
contract ReferenceTypes {
    // Arrays
    uint256[] public dynamicArray;           // dynamic size
    uint256[10] public fixedArray;           // fixed size

    // Mapping (key => value)
    mapping(address => uint256) public balances;
    mapping(address => mapping(address => uint256)) public allowances;

    // Struct
    struct User {
        string name;
        uint256 age;
        bool isActive;
    }

    mapping(address => User) public users;

    // Working with arrays
    function addToArray(uint256 _value) public {
        dynamicArray.push(_value);
    }

    function getArrayLength() public view returns (uint256) {
        return dynamicArray.length;
    }

    // Working with mappings
    function setBalance(address _user, uint256 _amount) public {
        balances[_user] = _amount;
    }

    // Working with structs
    function createUser(string memory _name, uint256 _age) public {
        users[msg.sender] = User({
            name: _name,
            age: _age,
            isActive: true
        });
    }
}
```

### 1.4 Functions

```solidity
contract Functions {
    uint256 public count;

    // State-changing function
    function increment() public {
        count += 1;
    }

    // View function (reads state, no gas when called externally)
    function getCount() public view returns (uint256) {
        return count;
    }

    // Pure function (no state access, no gas when called externally)
    function add(uint256 a, uint256 b) public pure returns (uint256) {
        return a + b;
    }

    // Payable function (can receive Ether)
    function deposit() public payable {
        // msg.value contains the amount sent
    }

    // Internal function (only callable from within contract)
    function _internalHelper() internal pure returns (uint256) {
        return 42;
    }

    // Private function (only callable from this contract, not inherited)
    function _privateHelper() private pure returns (uint256) {
        return 100;
    }

    // Multiple return values
    function getMultiple() public pure returns (uint256, bool, string memory) {
        return (42, true, "hello");
    }

    // Named returns
    function calculate(uint256 x) public pure returns (uint256 result) {
        result = x * 2;
        // implicit return
    }
}
```

**Visibility Modifiers**:

```
┌───────────┬──────────────┬────────────┬──────────────┐
│ Modifier  │ This Contract│ Derived    │ External     │
│           │              │ Contracts  │ Calls        │
├───────────┼──────────────┼────────────┼──────────────┤
│ public    │ ✅           │ ✅         │ ✅           │
│ external  │ ❌ (via this)│ ✅         │ ✅           │
│ internal  │ ✅           │ ✅         │ ❌           │
│ private   │ ✅           │ ❌         │ ❌           │
└───────────┴──────────────┴────────────┴──────────────┘
```

### 1.5 Modifiers

```solidity
contract Modifiers {
    address public owner;
    bool public paused;

    constructor() {
        owner = msg.sender;
    }

    // Modifier definition
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;  // Continue execution
    }

    modifier whenNotPaused() {
        require(!paused, "Contract is paused");
        _;
    }

    modifier validAddress(address _addr) {
        require(_addr != address(0), "Invalid address");
        _;
    }

    // Using modifiers
    function changeOwner(address _newOwner)
        public
        onlyOwner
        validAddress(_newOwner)
    {
        owner = _newOwner;
    }

    function pause() public onlyOwner {
        paused = true;
    }

    function unpause() public onlyOwner {
        paused = false;
    }

    function sensitiveOperation() public onlyOwner whenNotPaused {
        // Only owner can call when not paused
    }
}
```

### 1.6 Events

```solidity
contract Events {
    // Event declarations
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event StatusChanged(string oldStatus, string newStatus, uint256 timestamp);

    mapping(address => uint256) public balances;

    function transfer(address _to, uint256 _amount) public {
        require(balances[msg.sender] >= _amount, "Insufficient balance");

        balances[msg.sender] -= _amount;
        balances[_to] += _amount;

        // Emit event
        emit Transfer(msg.sender, _to, _amount);
    }

    function changeStatus(string memory _oldStatus, string memory _newStatus) public {
        emit StatusChanged(_oldStatus, _newStatus, block.timestamp);
    }
}
```

**ทำไมต้องใช้ Events?**
- **Logging**: บันทึกข้อมูลที่เกิดขึ้น (ถูกกว่า storage)
- **External listening**: Frontend/Indexer สามารถ subscribe ได้
- **Indexed parameters**: สามารถ filter/search ได้ (สูงสุด 3 indexed params)

### 1.7 Errors

```solidity
// Custom errors (Solidity 0.8.4+) - ประหยัด gas กว่า require message
error InsufficientBalance(uint256 available, uint256 required);
error Unauthorized(address caller);
error InvalidAmount(uint256 amount);

contract ErrorHandling {
    mapping(address => uint256) public balances;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    // Using custom errors
    function withdraw(uint256 _amount) public {
        if (balances[msg.sender] < _amount) {
            revert InsufficientBalance({
                available: balances[msg.sender],
                required: _amount
            });
        }

        balances[msg.sender] -= _amount;
        payable(msg.sender).transfer(_amount);
    }

    // Using require (traditional way)
    function deposit() public payable {
        require(msg.value > 0, "Must send ETH");
        balances[msg.sender] += msg.value;
    }

    // Using assert (for invariants)
    function criticalOperation() public {
        // assert should NEVER fail if code is correct
        assert(address(this).balance >= 0);
    }

    // Using revert
    function adminOnly() public {
        if (msg.sender != owner) {
            revert Unauthorized(msg.sender);
        }
    }
}
```

**Error Handling Methods**:

```
┌────────────┬──────────────────┬──────────────────┬────────────┐
│ Method     │ Gas Refund       │ Use Case         │ Gas Cost   │
├────────────┼──────────────────┼──────────────────┼────────────┤
│ require()  │ ✅ Yes           │ Input validation │ Medium     │
│ revert()   │ ✅ Yes           │ Complex logic    │ Low        │
│ assert()   │ ❌ No            │ Invariants       │ High       │
│ Custom err │ ✅ Yes           │ Modern way       │ Lowest     │
└────────────┴──────────────────┴──────────────────┴────────────┘
```

### 1.8 Inheritance

```solidity
// Base contract
contract Ownable {
    address public owner;

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function transferOwnership(address newOwner) public virtual onlyOwner {
        require(newOwner != address(0), "Invalid address");
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }
}

// Derived contract
contract MyToken is Ownable {
    string public name;

    constructor(string memory _name) {
        name = _name;
        // owner is already set by Ownable constructor
    }

    // Can use onlyOwner modifier from parent
    function updateName(string memory _newName) public onlyOwner {
        name = _newName;
    }

    // Override parent function
    function transferOwnership(address newOwner) public override onlyOwner {
        // Custom logic before calling parent
        require(newOwner != address(this), "Cannot transfer to contract");
        super.transferOwnership(newOwner);
    }
}

// Multiple inheritance
contract Pausable {
    bool public paused;

    modifier whenNotPaused() {
        require(!paused, "Paused");
        _;
    }

    function _pause() internal {
        paused = true;
    }
}

contract MyAdvancedToken is Ownable, Pausable {
    mapping(address => uint256) public balances;

    function transfer(address to, uint256 amount) public whenNotPaused {
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }

    function pause() public onlyOwner {
        _pause();
    }
}
```

### 1.9 Interfaces & Libraries

#### Interface

```solidity
// Interface - defines contract ABI
interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

// Using interface
contract TokenSwap {
    function swapTokens(address tokenAddress, uint256 amount) public {
        IERC20 token = IERC20(tokenAddress);
        require(token.balanceOf(msg.sender) >= amount, "Insufficient balance");

        // Call functions through interface
        token.transferFrom(msg.sender, address(this), amount);
    }
}
```

#### Library

```solidity
// Library - reusable code
library SafeMath {
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a, "SafeMath: addition overflow");
        return c;
    }

    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a, "SafeMath: subtraction overflow");
        return a - b;
    }

    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) return 0;
        uint256 c = a * b;
        require(c / a == b, "SafeMath: multiplication overflow");
        return c;
    }
}

// Using library
contract Calculator {
    using SafeMath for uint256;

    function calculate(uint256 a, uint256 b) public pure returns (uint256) {
        // Can call as a.add(b) instead of SafeMath.add(a, b)
        return a.add(b).mul(2);
    }
}
```

---

## ERC-20 Token Standard

### 2.1 ERC-20 คืออะไร?

**ERC-20** เป็น token standard สำหรับ **fungible tokens** (tokens ที่แลกเปลี่ยนกันได้ 1:1)

**Use cases**:
- Cryptocurrencies (USDT, USDC, DAI)
- Governance tokens
- Utility tokens
- Reward points

### 2.2 ERC-20 Interface

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20 {
    // Returns the total token supply
    function totalSupply() external view returns (uint256);

    // Returns the account balance of another account
    function balanceOf(address account) external view returns (uint256);

    // Transfers tokens to a specified address
    function transfer(address to, uint256 amount) external returns (bool);

    // Returns the amount which spender is still allowed to withdraw from owner
    function allowance(address owner, address spender) external view returns (uint256);

    // Allows spender to withdraw from your account multiple times, up to the amount
    function approve(address spender, uint256 amount) external returns (bool);

    // Transfers tokens from one address to another (requires approval)
    function transferFrom(address from, address to, uint256 amount) external returns (bool);

    // Events
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
```

### 2.3 Full ERC-20 Implementation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ERC20Token {
    // Token metadata
    string public name;
    string public symbol;
    uint8 public decimals;

    // State variables
    uint256 private _totalSupply;
    mapping(address => uint256) private _balances;
    mapping(address => mapping(address => uint256)) private _allowances;

    // Events
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    // Constructor
    constructor(
        string memory _name,
        string memory _symbol,
        uint8 _decimals,
        uint256 initialSupply
    ) {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;

        // Mint initial supply to deployer
        _mint(msg.sender, initialSupply);
    }

    // View functions
    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account) public view returns (uint256) {
        return _balances[account];
    }

    function allowance(address owner, address spender) public view returns (uint256) {
        return _allowances[owner][spender];
    }

    // Transfer functions
    function transfer(address to, uint256 amount) public returns (bool) {
        _transfer(msg.sender, to, amount);
        return true;
    }

    function approve(address spender, uint256 amount) public returns (bool) {
        _approve(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) public returns (bool) {
        // Check allowance
        uint256 currentAllowance = _allowances[from][msg.sender];
        require(currentAllowance >= amount, "ERC20: insufficient allowance");

        // Update allowance
        unchecked {
            _approve(from, msg.sender, currentAllowance - amount);
        }

        // Transfer
        _transfer(from, to, amount);
        return true;
    }

    // Internal functions
    function _transfer(address from, address to, uint256 amount) internal {
        require(from != address(0), "ERC20: transfer from zero address");
        require(to != address(0), "ERC20: transfer to zero address");

        uint256 fromBalance = _balances[from];
        require(fromBalance >= amount, "ERC20: insufficient balance");

        unchecked {
            _balances[from] = fromBalance - amount;
            _balances[to] += amount;
        }

        emit Transfer(from, to, amount);
    }

    function _approve(address owner, address spender, uint256 amount) internal {
        require(owner != address(0), "ERC20: approve from zero address");
        require(spender != address(0), "ERC20: approve to zero address");

        _allowances[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }

    function _mint(address account, uint256 amount) internal {
        require(account != address(0), "ERC20: mint to zero address");

        _totalSupply += amount;
        unchecked {
            _balances[account] += amount;
        }

        emit Transfer(address(0), account, amount);
    }

    function _burn(address account, uint256 amount) internal {
        require(account != address(0), "ERC20: burn from zero address");

        uint256 accountBalance = _balances[account];
        require(accountBalance >= amount, "ERC20: burn amount exceeds balance");

        unchecked {
            _balances[account] = accountBalance - amount;
            _totalSupply -= amount;
        }

        emit Transfer(account, address(0), amount);
    }
}
```

### 2.4 Extended ERC-20 with Minting & Burning

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./ERC20Token.sol";

contract ExtendedERC20 is ERC20Token {
    address public owner;

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor(
        string memory _name,
        string memory _symbol,
        uint8 _decimals,
        uint256 initialSupply
    ) ERC20Token(_name, _symbol, _decimals, initialSupply) {
        owner = msg.sender;
    }

    // Mint new tokens (only owner)
    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }

    // Burn tokens
    function burn(uint256 amount) public {
        _burn(msg.sender, amount);
    }

    // Burn tokens from another account (requires allowance)
    function burnFrom(address account, uint256 amount) public {
        uint256 currentAllowance = allowance(account, msg.sender);
        require(currentAllowance >= amount, "ERC20: insufficient allowance");

        unchecked {
            _approve(account, msg.sender, currentAllowance - amount);
        }

        _burn(account, amount);
    }

    // Transfer ownership
    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0), "Invalid address");
        owner = newOwner;
    }
}
```

### 2.5 ERC-20 Workflow Diagram

```
Transfer Workflow:
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  User A (has 100 tokens)                                     │
│    │                                                         │
│    │ 1. transfer(UserB, 50)                                 │
│    └──────────────────────────────►                         │
│                                   │                          │
│                                   │ 2. Check balance        │
│                                   │    require(100 >= 50)   │
│                                   │                          │
│                                   │ 3. Update balances      │
│                                   │    UserA: 100 - 50 = 50 │
│                                   │    UserB: 0 + 50 = 50   │
│                                   │                          │
│                                   │ 4. Emit Transfer event  │
│                                   └────────────────────────► │
│                                                              │
│  Result: UserA has 50, UserB has 50                         │
└──────────────────────────────────────────────────────────────┘

TransferFrom Workflow (with Approval):
┌──────────────────────────────────────────────────────────────┐
│  User A (has 100 tokens)                                     │
│    │                                                         │
│    │ 1. approve(DEX, 50)                                    │
│    └──────────────────────────────►                         │
│                                   │                          │
│                                   │ 2. Store allowance      │
│                                   │    allowances[A][DEX]=50│
│                                   │                          │
│  DEX Contract                     │                          │
│    │                              │                          │
│    │ 3. transferFrom(A, B, 30)   │                          │
│    └──────────────────────────────┤                          │
│                                   │ 4. Check allowance      │
│                                   │    require(50 >= 30)    │
│                                   │                          │
│                                   │ 5. Update allowance     │
│                                   │    allowances[A][DEX]=20│
│                                   │                          │
│                                   │ 6. Transfer tokens      │
│                                   │    A: 100-30=70         │
│                                   │    B: 0+30=30           │
│                                   └────────────────────────► │
└──────────────────────────────────────────────────────────────┘
```

---

## ERC-721 NFT Standard

### 3.1 ERC-721 คืออะไร?

**ERC-721** เป็น token standard สำหรับ **Non-Fungible Tokens (NFTs)** - tokens ที่ไม่สามารถแลกเปลี่ยนกันได้ 1:1 เพราะแต่ละ token มี uniqueness

**Use cases**:
- Digital art & collectibles
- Gaming items
- Real estate
- Identity documents

### 3.2 ERC-721 Interface

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC721 {
    // Events
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);
    event ApprovalForAll(address indexed owner, address indexed operator, bool approved);

    // Required functions
    function balanceOf(address owner) external view returns (uint256 balance);
    function ownerOf(uint256 tokenId) external view returns (address owner);
    function safeTransferFrom(address from, address to, uint256 tokenId, bytes calldata data) external;
    function safeTransferFrom(address from, address to, uint256 tokenId) external;
    function transferFrom(address from, address to, uint256 tokenId) external;
    function approve(address to, uint256 tokenId) external;
    function setApprovalForAll(address operator, bool approved) external;
    function getApproved(uint256 tokenId) external view returns (address operator);
    function isApprovedForAll(address owner, address operator) external view returns (bool);
}

// Metadata extension
interface IERC721Metadata {
    function name() external view returns (string memory);
    function symbol() external view returns (string memory);
    function tokenURI(uint256 tokenId) external view returns (string memory);
}

// Receiver interface (for safe transfers)
interface IERC721Receiver {
    function onERC721Received(
        address operator,
        address from,
        uint256 tokenId,
        bytes calldata data
    ) external returns (bytes4);
}
```

### 3.3 Full ERC-721 Implementation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ERC721Token {
    // Token name
    string public name;

    // Token symbol
    string public symbol;

    // Mapping from token ID to owner address
    mapping(uint256 => address) private _owners;

    // Mapping owner address to token count
    mapping(address => uint256) private _balances;

    // Mapping from token ID to approved address
    mapping(uint256 => address) private _tokenApprovals;

    // Mapping from owner to operator approvals
    mapping(address => mapping(address => bool)) private _operatorApprovals;

    // Mapping from token ID to token URI
    mapping(uint256 => string) private _tokenURIs;

    // Events
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);
    event ApprovalForAll(address indexed owner, address indexed operator, bool approved);

    constructor(string memory _name, string memory _symbol) {
        name = _name;
        symbol = _symbol;
    }

    // View functions
    function balanceOf(address owner) public view returns (uint256) {
        require(owner != address(0), "ERC721: address zero is not a valid owner");
        return _balances[owner];
    }

    function ownerOf(uint256 tokenId) public view returns (address) {
        address owner = _owners[tokenId];
        require(owner != address(0), "ERC721: invalid token ID");
        return owner;
    }

    function tokenURI(uint256 tokenId) public view returns (string memory) {
        require(_exists(tokenId), "ERC721: invalid token ID");
        return _tokenURIs[tokenId];
    }

    function getApproved(uint256 tokenId) public view returns (address) {
        require(_exists(tokenId), "ERC721: invalid token ID");
        return _tokenApprovals[tokenId];
    }

    function isApprovedForAll(address owner, address operator) public view returns (bool) {
        return _operatorApprovals[owner][operator];
    }

    // Approval functions
    function approve(address to, uint256 tokenId) public {
        address owner = ownerOf(tokenId);
        require(to != owner, "ERC721: approval to current owner");
        require(
            msg.sender == owner || isApprovedForAll(owner, msg.sender),
            "ERC721: approve caller is not token owner or approved for all"
        );

        _approve(to, tokenId);
    }

    function setApprovalForAll(address operator, bool approved) public {
        require(operator != msg.sender, "ERC721: approve to caller");
        _operatorApprovals[msg.sender][operator] = approved;
        emit ApprovalForAll(msg.sender, operator, approved);
    }

    // Transfer functions
    function transferFrom(address from, address to, uint256 tokenId) public {
        require(_isApprovedOrOwner(msg.sender, tokenId), "ERC721: caller is not token owner or approved");
        _transfer(from, to, tokenId);
    }

    function safeTransferFrom(address from, address to, uint256 tokenId) public {
        safeTransferFrom(from, to, tokenId, "");
    }

    function safeTransferFrom(address from, address to, uint256 tokenId, bytes memory data) public {
        require(_isApprovedOrOwner(msg.sender, tokenId), "ERC721: caller is not token owner or approved");
        _safeTransfer(from, to, tokenId, data);
    }

    // Internal functions
    function _exists(uint256 tokenId) internal view returns (bool) {
        return _owners[tokenId] != address(0);
    }

    function _isApprovedOrOwner(address spender, uint256 tokenId) internal view returns (bool) {
        address owner = ownerOf(tokenId);
        return (spender == owner || isApprovedForAll(owner, spender) || getApproved(tokenId) == spender);
    }

    function _transfer(address from, address to, uint256 tokenId) internal {
        require(ownerOf(tokenId) == from, "ERC721: transfer from incorrect owner");
        require(to != address(0), "ERC721: transfer to the zero address");

        // Clear approvals
        _approve(address(0), tokenId);

        // Update balances
        unchecked {
            _balances[from] -= 1;
            _balances[to] += 1;
        }

        // Update owner
        _owners[tokenId] = to;

        emit Transfer(from, to, tokenId);
    }

    function _safeTransfer(address from, address to, uint256 tokenId, bytes memory data) internal {
        _transfer(from, to, tokenId);
        require(_checkOnERC721Received(from, to, tokenId, data), "ERC721: transfer to non ERC721Receiver implementer");
    }

    function _approve(address to, uint256 tokenId) internal {
        _tokenApprovals[tokenId] = to;
        emit Approval(ownerOf(tokenId), to, tokenId);
    }

    function _mint(address to, uint256 tokenId) internal {
        require(to != address(0), "ERC721: mint to the zero address");
        require(!_exists(tokenId), "ERC721: token already minted");

        unchecked {
            _balances[to] += 1;
        }

        _owners[tokenId] = to;

        emit Transfer(address(0), to, tokenId);
    }

    function _burn(uint256 tokenId) internal {
        address owner = ownerOf(tokenId);

        // Clear approvals
        _approve(address(0), tokenId);

        unchecked {
            _balances[owner] -= 1;
        }

        delete _owners[tokenId];
        delete _tokenURIs[tokenId];

        emit Transfer(owner, address(0), tokenId);
    }

    function _setTokenURI(uint256 tokenId, string memory uri) internal {
        require(_exists(tokenId), "ERC721: invalid token ID");
        _tokenURIs[tokenId] = uri;
    }

    function _checkOnERC721Received(
        address from,
        address to,
        uint256 tokenId,
        bytes memory data
    ) private returns (bool) {
        if (to.code.length > 0) {
            try IERC721Receiver(to).onERC721Received(msg.sender, from, tokenId, data) returns (bytes4 retval) {
                return retval == IERC721Receiver.onERC721Received.selector;
            } catch (bytes memory reason) {
                if (reason.length == 0) {
                    revert("ERC721: transfer to non ERC721Receiver implementer");
                } else {
                    assembly {
                        revert(add(32, reason), mload(reason))
                    }
                }
            }
        } else {
            return true;
        }
    }
}

// Receiver interface
interface IERC721Receiver {
    function onERC721Received(
        address operator,
        address from,
        uint256 tokenId,
        bytes calldata data
    ) external returns (bytes4);
}
```

### 3.4 Extended ERC-721 with Minting

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./ERC721Token.sol";

contract MyNFT is ERC721Token {
    uint256 private _nextTokenId;
    address public owner;

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor() ERC721Token("MyNFT", "MNFT") {
        owner = msg.sender;
    }

    // Mint NFT
    function mint(address to, string memory uri) public onlyOwner returns (uint256) {
        uint256 tokenId = _nextTokenId++;
        _mint(to, tokenId);
        _setTokenURI(tokenId, uri);
        return tokenId;
    }

    // Batch mint
    function batchMint(address to, uint256 quantity, string memory baseURI) public onlyOwner {
        for (uint256 i = 0; i < quantity; i++) {
            uint256 tokenId = _nextTokenId++;
            _mint(to, tokenId);
            _setTokenURI(tokenId, string(abi.encodePacked(baseURI, _toString(tokenId))));
        }
    }

    // Burn NFT
    function burn(uint256 tokenId) public {
        require(ownerOf(tokenId) == msg.sender, "Not token owner");
        _burn(tokenId);
    }

    // Helper function
    function _toString(uint256 value) internal pure returns (string memory) {
        if (value == 0) {
            return "0";
        }
        uint256 temp = value;
        uint256 digits;
        while (temp != 0) {
            digits++;
            temp /= 10;
        }
        bytes memory buffer = new bytes(digits);
        while (value != 0) {
            digits -= 1;
            buffer[digits] = bytes1(uint8(48 + uint256(value % 10)));
            value /= 10;
        }
        return string(buffer);
    }
}
```

---

## ERC-1155 Multi-Token Standard

### 4.1 ERC-1155 คืออะไร?

**ERC-1155** เป็น **Multi-Token Standard** ที่สามารถจัดการทั้ง fungible และ non-fungible tokens ใน contract เดียวกัน

**ข้อดี**:
- **Batch operations**: Transfer multiple tokens ในครั้งเดียว (ประหยัด gas)
- **Flexibility**: รองรับทั้ง FT และ NFT
- **Efficiency**: Contract เดียวจัดการได้หลาย token types

**Use cases**:
- Gaming (items, currencies, characters)
- Multi-class NFTs
- DeFi protocols with multiple assets

### 4.2 ERC-1155 Interface

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC1155 {
    event TransferSingle(
        address indexed operator,
        address indexed from,
        address indexed to,
        uint256 id,
        uint256 value
    );

    event TransferBatch(
        address indexed operator,
        address indexed from,
        address indexed to,
        uint256[] ids,
        uint256[] values
    );

    event ApprovalForAll(address indexed account, address indexed operator, bool approved);

    event URI(string value, uint256 indexed id);

    function balanceOf(address account, uint256 id) external view returns (uint256);
    function balanceOfBatch(address[] calldata accounts, uint256[] calldata ids) external view returns (uint256[] memory);
    function setApprovalForAll(address operator, bool approved) external;
    function isApprovedForAll(address account, address operator) external view returns (bool);
    function safeTransferFrom(address from, address to, uint256 id, uint256 amount, bytes calldata data) external;
    function safeBatchTransferFrom(address from, address to, uint256[] calldata ids, uint256[] calldata amounts, bytes calldata data) external;
}

interface IERC1155MetadataURI {
    function uri(uint256 id) external view returns (string memory);
}

interface IERC1155Receiver {
    function onERC1155Received(
        address operator,
        address from,
        uint256 id,
        uint256 value,
        bytes calldata data
    ) external returns (bytes4);

    function onERC1155BatchReceived(
        address operator,
        address from,
        uint256[] calldata ids,
        uint256[] calldata values,
        bytes calldata data
    ) external returns (bytes4);
}
```

### 4.3 Full ERC-1155 Implementation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ERC1155Token {
    // Mapping from token ID to account balances
    mapping(uint256 => mapping(address => uint256)) private _balances;

    // Mapping from account to operator approvals
    mapping(address => mapping(address => bool)) private _operatorApprovals;

    // Mapping from token ID to URI
    mapping(uint256 => string) private _tokenURIs;

    // Events
    event TransferSingle(
        address indexed operator,
        address indexed from,
        address indexed to,
        uint256 id,
        uint256 value
    );

    event TransferBatch(
        address indexed operator,
        address indexed from,
        address indexed to,
        uint256[] ids,
        uint256[] values
    );

    event ApprovalForAll(address indexed account, address indexed operator, bool approved);
    event URI(string value, uint256 indexed id);

    // View functions
    function balanceOf(address account, uint256 id) public view returns (uint256) {
        require(account != address(0), "ERC1155: address zero is not a valid owner");
        return _balances[id][account];
    }

    function balanceOfBatch(
        address[] memory accounts,
        uint256[] memory ids
    ) public view returns (uint256[] memory) {
        require(accounts.length == ids.length, "ERC1155: accounts and ids length mismatch");

        uint256[] memory batchBalances = new uint256[](accounts.length);

        for (uint256 i = 0; i < accounts.length; ++i) {
            batchBalances[i] = balanceOf(accounts[i], ids[i]);
        }

        return batchBalances;
    }

    function isApprovedForAll(address account, address operator) public view returns (bool) {
        return _operatorApprovals[account][operator];
    }

    function uri(uint256 id) public view returns (string memory) {
        return _tokenURIs[id];
    }

    // Approval
    function setApprovalForAll(address operator, bool approved) public {
        require(msg.sender != operator, "ERC1155: setting approval status for self");
        _operatorApprovals[msg.sender][operator] = approved;
        emit ApprovalForAll(msg.sender, operator, approved);
    }

    // Transfer functions
    function safeTransferFrom(
        address from,
        address to,
        uint256 id,
        uint256 amount,
        bytes memory data
    ) public {
        require(
            from == msg.sender || isApprovedForAll(from, msg.sender),
            "ERC1155: caller is not token owner or approved"
        );
        _safeTransferFrom(from, to, id, amount, data);
    }

    function safeBatchTransferFrom(
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) public {
        require(
            from == msg.sender || isApprovedForAll(from, msg.sender),
            "ERC1155: caller is not token owner or approved"
        );
        _safeBatchTransferFrom(from, to, ids, amounts, data);
    }

    // Internal functions
    function _safeTransferFrom(
        address from,
        address to,
        uint256 id,
        uint256 amount,
        bytes memory data
    ) internal {
        require(to != address(0), "ERC1155: transfer to the zero address");

        address operator = msg.sender;

        uint256 fromBalance = _balances[id][from];
        require(fromBalance >= amount, "ERC1155: insufficient balance for transfer");

        unchecked {
            _balances[id][from] = fromBalance - amount;
        }
        _balances[id][to] += amount;

        emit TransferSingle(operator, from, to, id, amount);

        _doSafeTransferAcceptanceCheck(operator, from, to, id, amount, data);
    }

    function _safeBatchTransferFrom(
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) internal {
        require(ids.length == amounts.length, "ERC1155: ids and amounts length mismatch");
        require(to != address(0), "ERC1155: transfer to the zero address");

        address operator = msg.sender;

        for (uint256 i = 0; i < ids.length; ++i) {
            uint256 id = ids[i];
            uint256 amount = amounts[i];

            uint256 fromBalance = _balances[id][from];
            require(fromBalance >= amount, "ERC1155: insufficient balance for transfer");

            unchecked {
                _balances[id][from] = fromBalance - amount;
            }
            _balances[id][to] += amount;
        }

        emit TransferBatch(operator, from, to, ids, amounts);

        _doSafeBatchTransferAcceptanceCheck(operator, from, to, ids, amounts, data);
    }

    function _mint(
        address to,
        uint256 id,
        uint256 amount,
        bytes memory data
    ) internal {
        require(to != address(0), "ERC1155: mint to the zero address");

        address operator = msg.sender;

        _balances[id][to] += amount;
        emit TransferSingle(operator, address(0), to, id, amount);

        _doSafeTransferAcceptanceCheck(operator, address(0), to, id, amount, data);
    }

    function _mintBatch(
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) internal {
        require(to != address(0), "ERC1155: mint to the zero address");
        require(ids.length == amounts.length, "ERC1155: ids and amounts length mismatch");

        address operator = msg.sender;

        for (uint256 i = 0; i < ids.length; i++) {
            _balances[ids[i]][to] += amounts[i];
        }

        emit TransferBatch(operator, address(0), to, ids, amounts);

        _doSafeBatchTransferAcceptanceCheck(operator, address(0), to, ids, amounts, data);
    }

    function _burn(address from, uint256 id, uint256 amount) internal {
        require(from != address(0), "ERC1155: burn from the zero address");

        address operator = msg.sender;

        uint256 fromBalance = _balances[id][from];
        require(fromBalance >= amount, "ERC1155: burn amount exceeds balance");

        unchecked {
            _balances[id][from] = fromBalance - amount;
        }

        emit TransferSingle(operator, from, address(0), id, amount);
    }

    function _setURI(uint256 id, string memory newuri) internal {
        _tokenURIs[id] = newuri;
        emit URI(newuri, id);
    }

    function _doSafeTransferAcceptanceCheck(
        address operator,
        address from,
        address to,
        uint256 id,
        uint256 amount,
        bytes memory data
    ) private {
        if (to.code.length > 0) {
            try IERC1155Receiver(to).onERC1155Received(operator, from, id, amount, data) returns (bytes4 response) {
                if (response != IERC1155Receiver.onERC1155Received.selector) {
                    revert("ERC1155: ERC1155Receiver rejected tokens");
                }
            } catch Error(string memory reason) {
                revert(reason);
            } catch {
                revert("ERC1155: transfer to non-ERC1155Receiver implementer");
            }
        }
    }

    function _doSafeBatchTransferAcceptanceCheck(
        address operator,
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) private {
        if (to.code.length > 0) {
            try IERC1155Receiver(to).onERC1155BatchReceived(operator, from, ids, amounts, data) returns (bytes4 response) {
                if (response != IERC1155Receiver.onERC1155BatchReceived.selector) {
                    revert("ERC1155: ERC1155Receiver rejected tokens");
                }
            } catch Error(string memory reason) {
                revert(reason);
            } catch {
                revert("ERC1155: transfer to non-ERC1155Receiver implementer");
            }
        }
    }
}

interface IERC1155Receiver {
    function onERC1155Received(
        address operator,
        address from,
        uint256 id,
        uint256 value,
        bytes calldata data
    ) external returns (bytes4);

    function onERC1155BatchReceived(
        address operator,
        address from,
        uint256[] calldata ids,
        uint256[] calldata values,
        bytes calldata data
    ) external returns (bytes4);
}
```

### 4.4 Extended ERC-1155 Game Items Example

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./ERC1155Token.sol";

contract GameItems is ERC1155Token {
    address public owner;
    uint256 private _nextTokenId;

    // Token types
    uint256 public constant GOLD = 0;           // Fungible
    uint256 public constant SILVER = 1;         // Fungible
    uint256 public constant SWORD = 2;          // Semi-fungible
    uint256 public constant SHIELD = 3;         // Semi-fungible
    uint256 public constant UNIQUE_ITEM_START = 1000;  // NFTs start from 1000

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor() {
        owner = msg.sender;

        // Set URIs
        _setURI(GOLD, "https://game.example/api/item/0.json");
        _setURI(SILVER, "https://game.example/api/item/1.json");
        _setURI(SWORD, "https://game.example/api/item/2.json");
        _setURI(SHIELD, "https://game.example/api/item/3.json");
    }

    // Mint fungible tokens (e.g., gold, silver)
    function mintCurrency(address to, uint256 id, uint256 amount) public onlyOwner {
        require(id < UNIQUE_ITEM_START, "Use mintUnique for NFTs");
        _mint(to, id, amount, "");
    }

    // Mint unique item (NFT)
    function mintUnique(address to, string memory tokenURI) public onlyOwner returns (uint256) {
        uint256 tokenId = UNIQUE_ITEM_START + _nextTokenId++;
        _mint(to, tokenId, 1, "");
        _setURI(tokenId, tokenURI);
        return tokenId;
    }

    // Batch mint multiple items
    function mintBatch(
        address to,
        uint256[] memory ids,
        uint256[] memory amounts
    ) public onlyOwner {
        _mintBatch(to, ids, amounts, "");
    }

    // Burn tokens
    function burn(uint256 id, uint256 amount) public {
        _burn(msg.sender, id, amount);
    }

    // Craft item (burn ingredients, mint result)
    function craft(
        uint256[] memory ingredientIds,
        uint256[] memory ingredientAmounts,
        uint256 resultId,
        uint256 resultAmount
    ) public {
        // Burn ingredients
        for (uint256 i = 0; i < ingredientIds.length; i++) {
            _burn(msg.sender, ingredientIds[i], ingredientAmounts[i]);
        }

        // Mint result
        _mint(msg.sender, resultId, resultAmount, "");
    }
}
```

### 4.5 ERC Standard Comparison

```
┌──────────────┬──────────────┬──────────────┬──────────────────────┐
│ Feature      │ ERC-20       │ ERC-721      │ ERC-1155             │
├──────────────┼──────────────┼──────────────┼──────────────────────┤
│ Type         │ Fungible     │ Non-Fungible │ Multi (Both)         │
│ Token ID     │ No           │ Yes          │ Yes                  │
│ Decimals     │ Yes          │ No           │ No (but flexible)    │
│ Batch Ops    │ No           │ No           │ Yes                  │
│ Gas Cost     │ Low          │ Medium       │ Low (batch)          │
│ Use Case     │ Currency     │ Unique items │ Gaming, Multi-asset  │
│ Contract per │ One token    │ One project  │ Multiple tokens      │
│ Example      │ USDT, DAI    │ CryptoPunks  │ Enjin, Sandbox       │
└──────────────┴──────────────┴──────────────┴──────────────────────┘
```

---

## Foundry Development

### 5.1 Foundry คืออะไร?

**Foundry** เป็น development framework สำหรับ Ethereum ที่เขียนด้วย Rust ประกอบด้วย:

- **Forge**: Build, test, deploy contracts
- **Cast**: CLI tool สำหรับ interact กับ contracts
- **Anvil**: Local Ethereum node
- **Chisel**: Solidity REPL

### 5.2 Project Setup

```bash
# Create new Foundry project
forge init my-token-project
cd my-token-project

# Project structure
tree -L 2
```

```
my-token-project/
├── foundry.toml          # Configuration
├── src/                  # Contract source
│   └── Counter.sol
├── test/                 # Tests
│   └── Counter.t.sol
├── script/               # Deployment scripts
│   └── Counter.s.sol
└── lib/                  # Dependencies
```

### 5.3 Foundry Configuration

**foundry.toml**:

```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
solc_version = "0.8.20"
optimizer = true
optimizer_runs = 200
via_ir = false

[rpc_endpoints]
mainnet = "${MAINNET_RPC_URL}"
sepolia = "${SEPOLIA_RPC_URL}"
local = "http://localhost:8545"

[etherscan]
mainnet = { key = "${ETHERSCAN_API_KEY}" }
sepolia = { key = "${ETHERSCAN_API_KEY}" }

# Test configuration
[profile.default.fuzz]
runs = 256
max_test_rejects = 65536

[profile.default.invariant]
runs = 256
depth = 15
```

### 5.4 Installing Dependencies

```bash
# Install OpenZeppelin contracts
forge install OpenZeppelin/openzeppelin-contracts

# Install Solmate (gas-optimized contracts)
forge install transmissions11/solmate

# Update dependencies
forge update

# Remove dependency
forge remove openzeppelin-contracts
```

**Import in Solidity**:

```solidity
import "openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";
import "solmate/tokens/ERC721.sol";
```

### 5.5 Writing Tests

**test/MyToken.t.sol**:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "../src/ERC20Token.sol";

contract MyTokenTest is Test {
    ERC20Token public token;
    address public alice = address(0x1);
    address public bob = address(0x2);

    function setUp() public {
        // Runs before each test
        token = new ERC20Token("MyToken", "MTK", 18, 1000000 * 10**18);

        // Give Alice some tokens
        vm.prank(address(this));
        token.transfer(alice, 100 * 10**18);
    }

    function testInitialSupply() public {
        assertEq(token.totalSupply(), 1000000 * 10**18);
    }

    function testTransfer() public {
        vm.startPrank(alice);

        uint256 aliceBalanceBefore = token.balanceOf(alice);
        uint256 bobBalanceBefore = token.balanceOf(bob);

        token.transfer(bob, 10 * 10**18);

        assertEq(token.balanceOf(alice), aliceBalanceBefore - 10 * 10**18);
        assertEq(token.balanceOf(bob), bobBalanceBefore + 10 * 10**18);

        vm.stopPrank();
    }

    function testTransferInsufficientBalance() public {
        vm.startPrank(alice);

        // Expect revert
        vm.expectRevert("ERC20: insufficient balance");
        token.transfer(bob, 1000 * 10**18);

        vm.stopPrank();
    }

    function testApproveAndTransferFrom() public {
        vm.startPrank(alice);

        // Alice approves Bob to spend 50 tokens
        token.approve(bob, 50 * 10**18);
        assertEq(token.allowance(alice, bob), 50 * 10**18);

        vm.stopPrank();

        // Bob transfers from Alice
        vm.prank(bob);
        token.transferFrom(alice, bob, 30 * 10**18);

        assertEq(token.balanceOf(bob), 30 * 10**18);
        assertEq(token.allowance(alice, bob), 20 * 10**18);
    }

    function testEmitEvents() public {
        vm.startPrank(alice);

        // Expect Transfer event
        vm.expectEmit(true, true, false, true);
        emit Transfer(alice, bob, 10 * 10**18);

        token.transfer(bob, 10 * 10**18);

        vm.stopPrank();
    }

    // Fuzz testing - runs with random inputs
    function testFuzzTransfer(address to, uint256 amount) public {
        vm.assume(to != address(0));
        vm.assume(amount <= token.balanceOf(alice));

        vm.prank(alice);
        token.transfer(to, amount);

        assertEq(token.balanceOf(to), amount);
    }
}

event Transfer(address indexed from, address indexed to, uint256 value);
```

**Useful Test Functions**:

```solidity
// Cheat codes (vm)
vm.prank(address)              // Next call from address
vm.startPrank(address)         // All subsequent calls from address
vm.stopPrank()                 // Stop prank
vm.expectRevert()              // Expect next call to revert
vm.expectEmit()                // Expect event emission
vm.deal(address, amount)       // Give address ETH
vm.warp(timestamp)             // Set block.timestamp
vm.roll(blockNumber)           // Set block.number
vm.assume(condition)           // Fuzz test assumption

// Assertions
assertEq(a, b)                 // a == b
assertTrue(condition)          // condition is true
assertFalse(condition)         // condition is false
assertGt(a, b)                 // a > b
assertLt(a, b)                 // a < b
assertGe(a, b)                 // a >= b
assertLe(a, b)                 // a <= b
```

### 5.6 Running Tests

```bash
# Run all tests
forge test

# Run specific test
forge test --match-test testTransfer

# Run tests in specific file
forge test --match-path test/MyToken.t.sol

# Verbose output
forge test -vvvv

# Gas report
forge test --gas-report

# Coverage
forge coverage

# Watch mode (rerun on file changes)
forge test --watch
```

**Output verbosity**:

```
-v    Show test results
-vv   Show console.log output
-vvv  Show execution traces for failing tests
-vvvv Show execution traces for all tests
-vvvvv Show execution and setup traces for all tests
```

### 5.7 Deployment Scripts

**script/DeployMyToken.s.sol**:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "../src/ERC20Token.sol";

contract DeployMyToken is Script {
    function run() external {
        // Load private key from environment
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");

        vm.startBroadcast(deployerPrivateKey);

        // Deploy contract
        ERC20Token token = new ERC20Token(
            "MyToken",
            "MTK",
            18,
            1000000 * 10**18  // 1 million tokens
        );

        console.log("Token deployed at:", address(token));
        console.log("Total supply:", token.totalSupply());

        vm.stopBroadcast();
    }
}
```

**Deploy to local Anvil**:

```bash
# Start Anvil
anvil

# Deploy (in another terminal)
forge script script/DeployMyToken.s.sol:DeployMyToken \
  --rpc-url http://localhost:8545 \
  --broadcast \
  --private-key 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
```

**Deploy to testnet**:

```bash
# Deploy to Sepolia
forge script script/DeployMyToken.s.sol:DeployMyToken \
  --rpc-url $SEPOLIA_RPC_URL \
  --broadcast \
  --verify \
  --etherscan-api-key $ETHERSCAN_API_KEY
```

### 5.8 Gas Optimization

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract GasOptimization {
    // ❌ Expensive
    function badLoop(uint256[] memory data) public pure returns (uint256) {
        uint256 sum = 0;
        for (uint256 i = 0; i < data.length; i++) {
            sum += data[i];
        }
        return sum;
    }

    // ✅ Cheaper - cache array length
    function goodLoop(uint256[] memory data) public pure returns (uint256) {
        uint256 sum = 0;
        uint256 length = data.length;
        for (uint256 i = 0; i < length; i++) {
            sum += data[i];
        }
        return sum;
    }

    // ❌ Expensive - multiple SLOAD
    mapping(address => uint256) public balances;

    function badUpdate(address user, uint256 amount) public {
        balances[user] = balances[user] + amount;
        balances[user] = balances[user] * 2;
    }

    // ✅ Cheaper - single SLOAD, single SSTORE
    function goodUpdate(address user, uint256 amount) public {
        uint256 balance = balances[user];
        balance = balance + amount;
        balance = balance * 2;
        balances[user] = balance;
    }

    // ❌ Expensive - using += for storage
    function badIncrement() public {
        balances[msg.sender] += 1;
    }

    // ✅ Cheaper - using unchecked
    function goodIncrement() public {
        unchecked {
            balances[msg.sender] += 1;
        }
    }
}
```

**Gas Optimization Tips**:

```
┌─────────────────────────────────────────────────────────────┐
│ Technique                          │ Gas Saved              │
├─────────────────────────────────────────────────────────────┤
│ Use uint256 instead of smaller     │ ~5-10% per operation   │
│ Pack storage variables              │ ~20,000 per slot saved │
│ Cache storage variables in memory   │ ~100 gas per SLOAD     │
│ Use unchecked for safe operations   │ ~20-40 gas per op      │
│ Use custom errors instead of revert │ ~50 gas per error      │
│ Use calldata instead of memory      │ ~60 gas per param      │
│ Batch operations                    │ ~21,000 per tx saved   │
└─────────────────────────────────────────────────────────────┘
```

---

## Contract Interaction

### 6.1 Using Cast (Command Line)

```bash
# Get block number
cast block-number --rpc-url http://localhost:8545

# Get balance
cast balance 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb8 --rpc-url http://localhost:8545

# Call view function
cast call <CONTRACT_ADDRESS> "balanceOf(address)(uint256)" <USER_ADDRESS> --rpc-url http://localhost:8545

# Send transaction
cast send <CONTRACT_ADDRESS> "transfer(address,uint256)" <TO_ADDRESS> 1000000000000000000 \
  --rpc-url http://localhost:8545 \
  --private-key <PRIVATE_KEY>

# Get transaction receipt
cast receipt <TX_HASH> --rpc-url http://localhost:8545

# Decode transaction input
cast 4byte-decode <CALLDATA>

# Convert wei to ether
cast to-unit 1000000000000000000 ether

# Compute keccak256
cast keccak "Transfer(address,address,uint256)"
```

### 6.2 ABI Encoding/Decoding

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ABIExample {
    // Encode function call
    function encodeTransfer(address to, uint256 amount) public pure returns (bytes memory) {
        return abi.encodeWithSignature("transfer(address,uint256)", to, amount);
    }

    // Encode function call with selector
    function encodeTransferWithSelector(address to, uint256 amount) public pure returns (bytes memory) {
        return abi.encodeWithSelector(bytes4(keccak256("transfer(address,uint256)")), to, amount);
    }

    // Encode packed (for hashing)
    function encodePacked(address addr, uint256 value) public pure returns (bytes memory) {
        return abi.encodePacked(addr, value);
    }

    // Decode
    function decode(bytes memory data) public pure returns (address, uint256) {
        return abi.decode(data, (address, uint256));
    }
}
```

### 6.3 Calling Contracts from Solidity

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20 {
    function transfer(address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

contract ContractCaller {
    // Method 1: Using interface
    function callWithInterface(address tokenAddress, address to, uint256 amount) public {
        IERC20 token = IERC20(tokenAddress);
        bool success = token.transfer(to, amount);
        require(success, "Transfer failed");
    }

    // Method 2: Low-level call
    function callWithLowLevel(address tokenAddress, address to, uint256 amount) public {
        bytes memory data = abi.encodeWithSignature("transfer(address,uint256)", to, amount);

        (bool success, bytes memory returnData) = tokenAddress.call(data);
        require(success, "Transfer failed");

        bool result = abi.decode(returnData, (bool));
        require(result, "Transfer returned false");
    }

    // Method 3: delegatecall (execute code in this contract's context)
    function delegatecallExample(address implementation, bytes memory data) public {
        (bool success, bytes memory returnData) = implementation.delegatecall(data);
        require(success, "Delegatecall failed");
    }

    // Check if call will succeed (without executing)
    function staticCall(address tokenAddress, address account) public view returns (uint256) {
        (bool success, bytes memory returnData) = tokenAddress.staticcall(
            abi.encodeWithSignature("balanceOf(address)", account)
        );
        require(success, "Static call failed");
        return abi.decode(returnData, (uint256));
    }
}
```

### 6.4 Event Listening with Python

```python
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json

# Connect to node
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Contract ABI (simplified)
TOKEN_ABI = json.loads('''[
    {
        "anonymous": false,
        "inputs": [
            {"indexed": true, "name": "from", "type": "address"},
            {"indexed": true, "name": "to", "type": "address"},
            {"indexed": false, "name": "value", "type": "uint256"}
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]''')

# Contract instance
contract_address = '0x5FbDB2315678afecb367f032d93F642f64180aa3'
contract = w3.eth.contract(address=contract_address, abi=TOKEN_ABI)

# Read balance
user_address = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
balance = contract.functions.balanceOf(user_address).call()
print(f"Balance: {Web3.from_wei(balance, 'ether')} tokens")

# Send transaction
private_key = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'
account = w3.eth.account.from_key(private_key)

# Build transaction
tx = contract.functions.transfer(
    '0x70997970C51812dc3A010C7d01b50e0d17dc79C8',
    Web3.to_wei(10, 'ether')
).build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 100000,
    'gasPrice': w3.eth.gas_price
})

# Sign and send
signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(f"Transaction hash: {tx_hash.hex()}")

# Wait for receipt
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Transaction status: {receipt['status']}")

# Get past events
transfer_filter = contract.events.Transfer.create_filter(
    fromBlock=0,
    toBlock='latest',
    argument_filters={'from': user_address}
)

for event in transfer_filter.get_all_entries():
    print(f"Transfer: {event['args']['from']} -> {event['args']['to']}: {event['args']['value']}")

# Listen for new events
def handle_event(event):
    print(f"New transfer: {event['args']}")

event_filter = contract.events.Transfer.create_filter(fromBlock='latest')

while True:
    for event in event_filter.get_new_entries():
        handle_event(event)
    time.sleep(2)
```

---

## แบบฝึกหัด

### แบบฝึกหัดที่ 1: Deploy ERC-20 Token

**เป้าหมาย**: Deploy ERC-20 token ด้วย Foundry และทดสอบ

**ขั้นตอน**:

1. สร้าง Foundry project ใหม่
2. สร้าง ERC-20 contract ชื่อ "MyToken" (MTK)
3. เขียน tests สำหรับ:
   - Initial supply
   - Transfer
   - Approve & transferFrom
4. Deploy ไปที่ Anvil local node
5. Interact ด้วย cast

**Expected output**:
```bash
$ forge test
[PASS] testInitialSupply() (gas: 12345)
[PASS] testTransfer() (gas: 56789)
[PASS] testApproveAndTransferFrom() (gas: 98765)

$ forge script script/Deploy.s.sol --broadcast --rpc-url http://localhost:8545
Token deployed at: 0x5FbDB2315678afecb367f032d93F642f64180aa3
```

### แบบฝึกหัดที่ 2: NFT Collection

**เป้าหมาย**: สร้าง NFT collection พร้อม metadata

**Requirements**:
- ERC-721 contract
- Max supply: 10,000 NFTs
- Public mint function (0.01 ETH per NFT)
- Owner can withdraw funds
- Token URI: `https://api.example.com/metadata/{tokenId}`

**Pass criteria**:
- ✅ Contract deployed successfully
- ✅ Can mint NFT with 0.01 ETH
- ✅ Cannot mint more than max supply
- ✅ Token URI returns correct format
- ✅ Owner can withdraw funds

### แบบฝึกหัดที่ 3: Multi-Token Game Items

**เป้าหมาย**: สร้าง ERC-1155 contract สำหรับเกม

**Requirements**:
- Token types: Gold (ID=0), Silver (ID=1), Sword (ID=2), Unique Items (ID>=1000)
- Admin can mint fungible tokens
- Users can craft: 100 Gold + 50 Silver = 1 Sword
- Batch transfer support

**Pass criteria**:
- ✅ Can mint gold and silver
- ✅ Crafting burns ingredients and mints result
- ✅ Batch transfer works
- ✅ Can mint unique items

### แบบฝึกหัดที่ 4: Token Swap Contract

**เป้าหมาย**: สร้าง simple token swap contract

**Requirements**:
- Swap Token A for Token B (1:2 ratio)
- Contract holds liquidity pool
- Users approve tokens before swap
- Emit Swap event

**Pass criteria**:
- ✅ Contract can receive both tokens
- ✅ Swap works at correct ratio
- ✅ Reverts if insufficient liquidity
- ✅ Reverts if user has insufficient balance

### แบบฝึกหัดที่ 5: Event Indexer Script

**เป้าหมาย**: เขียน Python script ที่ listen และบันทึก Transfer events

**Requirements**:
- Connect to local Anvil node
- Listen for ERC-20 Transfer events
- Save to SQLite database
- Display live updates

**Expected output**:
```
Connected to Anvil node (Chain ID: 31337)
Listening for Transfer events on 0x5FbDB2315678afecb367f032d93F642f64180aa3...

[Block 123] Transfer: 0xf39F...92266 -> 0x7099...dc79C8 (10.0 MTK)
[Block 124] Transfer: 0x7099...dc79C8 -> 0x3C44...b073 (5.0 MTK)
```

---

## Pass Criteria - PART03

ก่อนจบ PART03 ให้ตรวจสอบว่า:

- [ ] เข้าใจพื้นฐาน Solidity (types, functions, modifiers, events)
- [ ] เข้าใจ ERC-20 standard และสามารถ implement ได้
- [ ] เข้าใจ ERC-721 standard และสามารถ implement ได้
- [ ] เข้าใจ ERC-1155 standard และแตกต่างจาก ERC-20/721 อย่างไร
- [ ] สามารถใช้ Foundry (forge, cast, anvil) ได้
- [ ] เขียน tests ด้วย Forge ได้
- [ ] Deploy contracts ด้วย Forge scripts ได้
- [ ] Interact กับ contracts ด้วย Cast และ Python (web3.py)
- [ ] สามารถทำแบบฝึกหัดอย่างน้อย 3 ข้อให้สำเร็จ

---

## Production Notes

### Security Considerations

1. **Reentrancy**: ใช้ ReentrancyGuard สำหรับ functions ที่ transfer ETH
2. **Integer Overflow**: Solidity 0.8+ มี built-in overflow protection (แต่ใช้ `unchecked` อย่างระวัง)
3. **Access Control**: ใช้ modifiers เช่น `onlyOwner` อย่างเหมาะสม
4. **Front-running**: ระวัง MEV attacks ใน DEX/AMM contracts
5. **Gas Limits**: ระวัง unbounded loops ที่อาจเกิน block gas limit

### Gas Optimization Checklist

- [ ] Use `uint256` instead of smaller uints
- [ ] Pack storage variables
- [ ] Cache storage variables in memory/stack
- [ ] Use `unchecked` for safe arithmetic
- [ ] Use custom errors instead of revert strings
- [ ] Use `calldata` instead of `memory` for external functions
- [ ] Batch operations when possible
- [ ] Avoid unnecessary SLOADs/SSTOREs

### Testing Best Practices

- Unit tests coverage ≥ 80%
- Test all edge cases และ error conditions
- Fuzz testing สำหรับ critical functions
- Integration tests กับ real contracts
- Gas benchmarking
- Invariant testing

### Deployment Checklist

- [ ] Audit code (internal + external)
- [ ] Test on testnet (Sepolia/Goerli)
- [ ] Verify contract on Etherscan
- [ ] Setup monitoring (Tenderly/Defender)
- [ ] Prepare upgrade strategy (if using proxies)
- [ ] Document all functions (NatSpec)

---

## Resources

- **Solidity Docs**: https://docs.soliditylang.org
- **OpenZeppelin**: https://docs.openzeppelin.com/contracts
- **Foundry Book**: https://book.getfoundry.sh
- **Ethereum.org**: https://ethereum.org/en/developers/docs/
- **Solidity by Example**: https://solidity-by-example.org

---

**จบ PART03 - Smart Contracts & Solidity**

**ถัดไป**: PART04 - Database Design & Schema (PostgreSQL, ClickHouse, Indexing Strategy)

---

**สถิติ PART03**:
- **Lines**: ~2,055 lines
- **Contracts**: 10+ complete implementations
- **Examples**: 50+ code snippets
- **Exercises**: 5 hands-on labs

---

*เอกสารนี้เป็นส่วนหนึ่งของโปรเจกต์ Blockchain Explorer System*
*สามารถดู source code ทั้งหมดได้ที่: [Repository URL]*
