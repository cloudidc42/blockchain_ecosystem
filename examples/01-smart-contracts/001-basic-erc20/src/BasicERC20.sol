// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title BasicERC20
 * @dev ERC-20 Token implementation พร้อม mint, burn, และ pause
 * @notice Token พื้นฐานที่มีฟีเจอร์ครบถ้วนสำหรับการเรียนรู้
 */
contract BasicERC20 {
    // ========================================
    // State Variables
    // ========================================

    string public name;
    string public symbol;
    uint8 public constant decimals = 18;
    uint256 private _totalSupply;

    address public owner;
    bool public paused;

    mapping(address => uint256) private _balances;
    mapping(address => mapping(address => uint256)) private _allowances;

    // ========================================
    // Events
    // ========================================

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Mint(address indexed to, uint256 amount);
    event Burn(address indexed from, uint256 amount);
    event Paused(address account);
    event Unpaused(address account);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    // ========================================
    // Errors
    // ========================================

    error ERC20InsufficientBalance(address sender, uint256 balance, uint256 needed);
    error ERC20InvalidSender(address sender);
    error ERC20InvalidReceiver(address receiver);
    error ERC20InsufficientAllowance(address spender, uint256 allowance, uint256 needed);
    error ERC20InvalidApprover(address approver);
    error ERC20InvalidSpender(address spender);
    error EnforcedPause();
    error ExpectedPause();
    error OwnableUnauthorizedAccount(address account);
    error OwnableInvalidOwner(address owner);

    // ========================================
    // Modifiers
    // ========================================

    modifier onlyOwner() {
        if (msg.sender != owner) {
            revert OwnableUnauthorizedAccount(msg.sender);
        }
        _;
    }

    modifier whenNotPaused() {
        if (paused) {
            revert EnforcedPause();
        }
        _;
    }

    modifier whenPaused() {
        if (!paused) {
            revert ExpectedPause();
        }
        _;
    }

    // ========================================
    // Constructor
    // ========================================

    /**
     * @dev สร้าง token ใหม่
     * @param name_ ชื่อ token
     * @param symbol_ สัญลักษณ์ token
     * @param initialSupply จำนวน tokens เริ่มต้น (รวม decimals)
     */
    constructor(string memory name_, string memory symbol_, uint256 initialSupply) {
        if (msg.sender == address(0)) {
            revert OwnableInvalidOwner(address(0));
        }

        name = name_;
        symbol = symbol_;
        owner = msg.sender;
        paused = false;

        if (initialSupply > 0) {
            _mint(msg.sender, initialSupply);
        }
    }

    // ========================================
    // ERC-20 View Functions
    // ========================================

    /**
     * @dev ดู total supply
     */
    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    /**
     * @dev ดู balance ของ account
     */
    function balanceOf(address account) public view returns (uint256) {
        return _balances[account];
    }

    /**
     * @dev ดู allowance ที่ owner อนุมัติให้ spender
     */
    function allowance(address owner_, address spender) public view returns (uint256) {
        return _allowances[owner_][spender];
    }

    // ========================================
    // ERC-20 Transfer Functions
    // ========================================

    /**
     * @dev โอน tokens ให้ address อื่น
     * @param to ผู้รับ
     * @param value จำนวน tokens
     */
    function transfer(address to, uint256 value) public whenNotPaused returns (bool) {
        address sender = msg.sender;
        _transfer(sender, to, value);
        return true;
    }

    /**
     * @dev อนุมัติให้ spender ใช้ tokens ของเรา
     * @param spender ผู้ใช้จ่าย
     * @param value จำนวนที่อนุมัติ
     */
    function approve(address spender, uint256 value) public returns (bool) {
        address sender = msg.sender;
        _approve(sender, spender, value);
        return true;
    }

    /**
     * @dev โอน tokens จาก address อื่นที่อนุมัติเราไว้
     * @param from ผู้ส่ง
     * @param to ผู้รับ
     * @param value จำนวน tokens
     */
    function transferFrom(address from, address to, uint256 value) public whenNotPaused returns (bool) {
        address spender = msg.sender;
        _spendAllowance(from, spender, value);
        _transfer(from, to, value);
        return true;
    }

    // ========================================
    // Minting & Burning
    // ========================================

    /**
     * @dev สร้าง tokens ใหม่ (เฉพาะ owner)
     * @param to ผู้รับ tokens
     * @param amount จำนวน tokens
     */
    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }

    /**
     * @dev ทำลาย tokens ของตัวเอง
     * @param value จำนวน tokens ที่จะทำลาย
     */
    function burn(uint256 value) public {
        _burn(msg.sender, value);
    }

    /**
     * @dev ทำลาย tokens ของ account ที่อนุมัติเราไว้
     * @param account เจ้าของ tokens
     * @param value จำนวน tokens ที่จะทำลาย
     */
    function burnFrom(address account, uint256 value) public {
        _spendAllowance(account, msg.sender, value);
        _burn(account, value);
    }

    // ========================================
    // Pausable Functions
    // ========================================

    /**
     * @dev หยุดการทำงานของ contract ชั่วคราว
     */
    function pause() public onlyOwner whenNotPaused {
        paused = true;
        emit Paused(msg.sender);
    }

    /**
     * @dev เปิดการทำงานของ contract อีกครั้ง
     */
    function unpause() public onlyOwner whenPaused {
        paused = false;
        emit Unpaused(msg.sender);
    }

    // ========================================
    // Ownership Functions
    // ========================================

    /**
     * @dev โอนความเป็นเจ้าของ contract
     * @param newOwner เจ้าของใหม่
     */
    function transferOwnership(address newOwner) public onlyOwner {
        if (newOwner == address(0)) {
            revert OwnableInvalidOwner(address(0));
        }
        _transferOwnership(newOwner);
    }

    /**
     * @dev สละความเป็นเจ้าของ contract (ระวัง!)
     */
    function renounceOwnership() public onlyOwner {
        _transferOwnership(address(0));
    }

    // ========================================
    // Internal Functions
    // ========================================

    /**
     * @dev Internal transfer function
     */
    function _transfer(address from, address to, uint256 value) internal {
        if (from == address(0)) {
            revert ERC20InvalidSender(address(0));
        }
        if (to == address(0)) {
            revert ERC20InvalidReceiver(address(0));
        }

        uint256 fromBalance = _balances[from];
        if (fromBalance < value) {
            revert ERC20InsufficientBalance(from, fromBalance, value);
        }

        unchecked {
            _balances[from] = fromBalance - value;
            _balances[to] += value;
        }

        emit Transfer(from, to, value);
    }

    /**
     * @dev Internal mint function
     */
    function _mint(address account, uint256 value) internal {
        if (account == address(0)) {
            revert ERC20InvalidReceiver(address(0));
        }

        _totalSupply += value;
        unchecked {
            _balances[account] += value;
        }

        emit Transfer(address(0), account, value);
        emit Mint(account, value);
    }

    /**
     * @dev Internal burn function
     */
    function _burn(address account, uint256 value) internal {
        if (account == address(0)) {
            revert ERC20InvalidSender(address(0));
        }

        uint256 accountBalance = _balances[account];
        if (accountBalance < value) {
            revert ERC20InsufficientBalance(account, accountBalance, value);
        }

        unchecked {
            _balances[account] = accountBalance - value;
            _totalSupply -= value;
        }

        emit Transfer(account, address(0), value);
        emit Burn(account, value);
    }

    /**
     * @dev Internal approve function
     */
    function _approve(address owner_, address spender, uint256 value) internal {
        if (owner_ == address(0)) {
            revert ERC20InvalidApprover(address(0));
        }
        if (spender == address(0)) {
            revert ERC20InvalidSpender(address(0));
        }

        _allowances[owner_][spender] = value;
        emit Approval(owner_, spender, value);
    }

    /**
     * @dev Internal spend allowance function
     */
    function _spendAllowance(address owner_, address spender, uint256 value) internal {
        uint256 currentAllowance = allowance(owner_, spender);
        if (currentAllowance != type(uint256).max) {
            if (currentAllowance < value) {
                revert ERC20InsufficientAllowance(spender, currentAllowance, value);
            }
            unchecked {
                _approve(owner_, spender, currentAllowance - value);
            }
        }
    }

    /**
     * @dev Internal ownership transfer function
     */
    function _transferOwnership(address newOwner) internal {
        address oldOwner = owner;
        owner = newOwner;
        emit OwnershipTransferred(oldOwner, newOwner);
    }
}
