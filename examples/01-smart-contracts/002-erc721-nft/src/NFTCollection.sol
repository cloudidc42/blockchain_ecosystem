// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title NFTCollection
 * @dev ERC-721 NFT Collection พร้อม minting, metadata, royalty, และ reveal mechanism
 * @notice NFT Collection แบบครบวงจรสำหรับการสร้าง NFT project
 */
contract NFTCollection {
    // ========================================
    // ERC-721 Storage
    // ========================================

    string public name;
    string public symbol;

    uint256 private _currentTokenId;
    uint256 public maxSupply;
    uint256 public mintPrice;

    address public owner;
    bool public paused;
    bool public revealed;

    string private _baseTokenURI;
    string private _unrevealedURI;

    // Royalty (EIP-2981)
    address public royaltyReceiver;
    uint96 public royaltyBasisPoints; // 10000 = 100%

    // Whitelist
    mapping(address => bool) public whitelist;
    bool public whitelistEnabled;

    mapping(uint256 => address) private _owners;
    mapping(address => uint256) private _balances;
    mapping(uint256 => address) private _tokenApprovals;
    mapping(address => mapping(address => bool)) private _operatorApprovals;

    // ========================================
    // Events
    // ========================================

    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);
    event ApprovalForAll(address indexed owner, address indexed operator, bool approved);
    event Minted(address indexed to, uint256 tokenId);
    event Revealed(string baseURI);
    event WhitelistUpdated(address indexed account, bool status);

    // ========================================
    // Errors
    // ========================================

    error NotOwnerOrApproved();
    error TokenNotFound();
    error InvalidAddress();
    error MintPriceNotMet();
    error MaxSupplyReached();
    error ContractPaused();
    error NotWhitelisted();
    error OnlyOwner();
    error InvalidTokenId();
    error TransferToZeroAddress();
    error MintToZeroAddress();

    // ========================================
    // Modifiers
    // ========================================

    modifier onlyOwner() {
        if (msg.sender != owner) revert OnlyOwner();
        _;
    }

    modifier whenNotPaused() {
        if (paused) revert ContractPaused();
        _;
    }

    // ========================================
    // Constructor
    // ========================================

    constructor(
        string memory name_,
        string memory symbol_,
        uint256 maxSupply_,
        uint256 mintPrice_,
        string memory unrevealedURI_
    ) {
        name = name_;
        symbol = symbol_;
        maxSupply = maxSupply_;
        mintPrice = mintPrice_;
        _unrevealedURI = unrevealedURI_;

        owner = msg.sender;
        royaltyReceiver = msg.sender;
        royaltyBasisPoints = 250; // 2.5% default

        paused = false;
        revealed = false;
        whitelistEnabled = false;
    }

    // ========================================
    // ERC-721 View Functions
    // ========================================

    function balanceOf(address owner_) public view returns (uint256) {
        if (owner_ == address(0)) revert InvalidAddress();
        return _balances[owner_];
    }

    function ownerOf(uint256 tokenId) public view returns (address) {
        address tokenOwner = _owners[tokenId];
        if (tokenOwner == address(0)) revert TokenNotFound();
        return tokenOwner;
    }

    function getApproved(uint256 tokenId) public view returns (address) {
        if (_owners[tokenId] == address(0)) revert TokenNotFound();
        return _tokenApprovals[tokenId];
    }

    function isApprovedForAll(address owner_, address operator) public view returns (bool) {
        return _operatorApprovals[owner_][operator];
    }

    function tokenURI(uint256 tokenId) public view returns (string memory) {
        if (_owners[tokenId] == address(0)) revert TokenNotFound();

        if (!revealed) {
            return _unrevealedURI;
        }

        return string(abi.encodePacked(_baseTokenURI, _toString(tokenId), ".json"));
    }

    function totalSupply() public view returns (uint256) {
        return _currentTokenId;
    }

    // ========================================
    // ERC-721 Transfer Functions
    // ========================================

    function approve(address to, uint256 tokenId) public {
        address tokenOwner = ownerOf(tokenId);

        if (to == tokenOwner) revert InvalidAddress();
        if (msg.sender != tokenOwner && !isApprovedForAll(tokenOwner, msg.sender)) {
            revert NotOwnerOrApproved();
        }

        _tokenApprovals[tokenId] = to;
        emit Approval(tokenOwner, to, tokenId);
    }

    function setApprovalForAll(address operator, bool approved) public {
        if (operator == msg.sender) revert InvalidAddress();
        _operatorApprovals[msg.sender][operator] = approved;
        emit ApprovalForAll(msg.sender, operator, approved);
    }

    function transferFrom(address from, address to, uint256 tokenId) public {
        if (!_isApprovedOrOwner(msg.sender, tokenId)) revert NotOwnerOrApproved();
        _transfer(from, to, tokenId);
    }

    function safeTransferFrom(address from, address to, uint256 tokenId) public {
        safeTransferFrom(from, to, tokenId, "");
    }

    function safeTransferFrom(address from, address to, uint256 tokenId, bytes memory data) public {
        if (!_isApprovedOrOwner(msg.sender, tokenId)) revert NotOwnerOrApproved();
        _transfer(from, to, tokenId);

        // Check if receiver is contract
        uint256 size;
        assembly { size := extcodesize(to) }
        if (size > 0) {
            // Call onERC721Received
            try IERC721Receiver(to).onERC721Received(msg.sender, from, tokenId, data) returns (bytes4 retval) {
                if (retval != IERC721Receiver.onERC721Received.selector) {
                    revert("ERC721: transfer to non ERC721Receiver");
                }
            } catch {
                revert("ERC721: transfer to non ERC721Receiver");
            }
        }
    }

    // ========================================
    // Minting Functions
    // ========================================

    function mint() public payable whenNotPaused returns (uint256) {
        if (_currentTokenId >= maxSupply) revert MaxSupplyReached();
        if (msg.value < mintPrice) revert MintPriceNotMet();
        if (whitelistEnabled && !whitelist[msg.sender]) revert NotWhitelisted();

        _currentTokenId++;
        uint256 tokenId = _currentTokenId;

        _mint(msg.sender, tokenId);

        return tokenId;
    }

    function mintBatch(uint256 amount) public payable whenNotPaused returns (uint256[] memory) {
        if (_currentTokenId + amount > maxSupply) revert MaxSupplyReached();
        if (msg.value < mintPrice * amount) revert MintPriceNotMet();
        if (whitelistEnabled && !whitelist[msg.sender]) revert NotWhitelisted();

        uint256[] memory tokenIds = new uint256[](amount);

        for (uint256 i = 0; i < amount; i++) {
            _currentTokenId++;
            uint256 tokenId = _currentTokenId;
            _mint(msg.sender, tokenId);
            tokenIds[i] = tokenId;
        }

        return tokenIds;
    }

    function ownerMint(address to, uint256 amount) public onlyOwner {
        if (_currentTokenId + amount > maxSupply) revert MaxSupplyReached();

        for (uint256 i = 0; i < amount; i++) {
            _currentTokenId++;
            uint256 tokenId = _currentTokenId;
            _mint(to, tokenId);
        }
    }

    // ========================================
    // Admin Functions
    // ========================================

    function reveal(string memory baseURI_) public onlyOwner {
        revealed = true;
        _baseTokenURI = baseURI_;
        emit Revealed(baseURI_);
    }

    function setUnrevealedURI(string memory uri) public onlyOwner {
        _unrevealedURI = uri;
    }

    function setMintPrice(uint256 price) public onlyOwner {
        mintPrice = price;
    }

    function pause() public onlyOwner {
        paused = true;
    }

    function unpause() public onlyOwner {
        paused = false;
    }

    function setWhitelistEnabled(bool enabled) public onlyOwner {
        whitelistEnabled = enabled;
    }

    function addToWhitelist(address[] calldata addresses) public onlyOwner {
        for (uint256 i = 0; i < addresses.length; i++) {
            whitelist[addresses[i]] = true;
            emit WhitelistUpdated(addresses[i], true);
        }
    }

    function removeFromWhitelist(address[] calldata addresses) public onlyOwner {
        for (uint256 i = 0; i < addresses.length; i++) {
            whitelist[addresses[i]] = false;
            emit WhitelistUpdated(addresses[i], false);
        }
    }

    function setRoyalty(address receiver, uint96 basisPoints) public onlyOwner {
        require(basisPoints <= 10000, "Royalty too high");
        royaltyReceiver = receiver;
        royaltyBasisPoints = basisPoints;
    }

    function withdraw() public onlyOwner {
        uint256 balance = address(this).balance;
        (bool success, ) = payable(owner).call{value: balance}("");
        require(success, "Withdraw failed");
    }

    function transferOwnership(address newOwner) public onlyOwner {
        if (newOwner == address(0)) revert InvalidAddress();
        owner = newOwner;
    }

    // ========================================
    // EIP-2981 Royalty
    // ========================================

    function royaltyInfo(uint256, uint256 salePrice) public view returns (address, uint256) {
        uint256 royaltyAmount = (salePrice * royaltyBasisPoints) / 10000;
        return (royaltyReceiver, royaltyAmount);
    }

    // ========================================
    // Internal Functions
    // ========================================

    function _mint(address to, uint256 tokenId) internal {
        if (to == address(0)) revert MintToZeroAddress();
        require(_owners[tokenId] == address(0), "Token already minted");

        _balances[to]++;
        _owners[tokenId] = to;

        emit Transfer(address(0), to, tokenId);
        emit Minted(to, tokenId);
    }

    function _transfer(address from, address to, uint256 tokenId) internal {
        if (ownerOf(tokenId) != from) revert NotOwnerOrApproved();
        if (to == address(0)) revert TransferToZeroAddress();

        // Clear approval
        delete _tokenApprovals[tokenId];

        _balances[from]--;
        _balances[to]++;
        _owners[tokenId] = to;

        emit Transfer(from, to, tokenId);
    }

    function _isApprovedOrOwner(address spender, uint256 tokenId) internal view returns (bool) {
        address tokenOwner = ownerOf(tokenId);
        return (spender == tokenOwner ||
                getApproved(tokenId) == spender ||
                isApprovedForAll(tokenOwner, spender));
    }

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

    // ========================================
    // ERC-165 Support
    // ========================================

    function supportsInterface(bytes4 interfaceId) public pure returns (bool) {
        return interfaceId == 0x01ffc9a7 || // ERC-165
               interfaceId == 0x80ac58cd || // ERC-721
               interfaceId == 0x2a55205a;   // EIP-2981
    }
}

// ========================================
// Interface
// ========================================

interface IERC721Receiver {
    function onERC721Received(
        address operator,
        address from,
        uint256 tokenId,
        bytes calldata data
    ) external returns (bytes4);
}
