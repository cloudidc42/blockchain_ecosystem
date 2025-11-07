// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "../src/NFTCollection.sol";

contract NFTCollectionTest is Test {
    NFTCollection public nft;

    address public owner;
    address public user1;
    address public user2;

    uint256 constant MAX_SUPPLY = 100;
    uint256 constant MINT_PRICE = 0.1 ether;
    string constant UNREVEALED_URI = "ipfs://unrevealed/metadata.json";

    event Minted(address indexed to, uint256 tokenId);
    event Revealed(string baseURI);

    function setUp() public {
        owner = address(this);
        user1 = makeAddr("user1");
        user2 = makeAddr("user2");

        nft = new NFTCollection("Test NFT", "TNFT", MAX_SUPPLY, MINT_PRICE, UNREVEALED_URI);

        // Fund test users
        vm.deal(user1, 100 ether);
        vm.deal(user2, 100 ether);
    }

    // ========================================
    // Constructor Tests
    // ========================================

    function testConstructor() public {
        assertEq(nft.name(), "Test NFT");
        assertEq(nft.symbol(), "TNFT");
        assertEq(nft.maxSupply(), MAX_SUPPLY);
        assertEq(nft.mintPrice(), MINT_PRICE);
        assertEq(nft.owner(), owner);
        assertEq(nft.totalSupply(), 0);
        assertFalse(nft.revealed());
        assertFalse(nft.paused());
    }

    // ========================================
    // Minting Tests
    // ========================================

    function testMint() public {
        vm.prank(user1);
        uint256 tokenId = nft.mint{value: MINT_PRICE}();

        assertEq(tokenId, 1);
        assertEq(nft.ownerOf(tokenId), user1);
        assertEq(nft.balanceOf(user1), 1);
        assertEq(nft.totalSupply(), 1);
    }

    function testMintInsufficientPayment() public {
        vm.prank(user1);
        vm.expectRevert(NFTCollection.MintPriceNotMet.selector);
        nft.mint{value: MINT_PRICE - 1}();
    }

    function testMintMaxSupply() public {
        // Mint all tokens
        nft.ownerMint(user1, MAX_SUPPLY);

        // Try to mint one more
        vm.prank(user2);
        vm.expectRevert(NFTCollection.MaxSupplyReached.selector);
        nft.mint{value: MINT_PRICE}();
    }

    function testMintBatch() public {
        uint256 amount = 5;

        vm.prank(user1);
        uint256[] memory tokenIds = nft.mintBatch{value: MINT_PRICE * amount}(amount);

        assertEq(tokenIds.length, amount);
        assertEq(nft.balanceOf(user1), amount);
        assertEq(nft.totalSupply(), amount);

        for (uint256 i = 0; i < amount; i++) {
            assertEq(tokenIds[i], i + 1);
            assertEq(nft.ownerOf(tokenIds[i]), user1);
        }
    }

    function testOwnerMint() public {
        nft.ownerMint(user1, 10);

        assertEq(nft.balanceOf(user1), 10);
        assertEq(nft.totalSupply(), 10);
    }

    function testOwnerMintOnlyOwner() public {
        vm.prank(user1);
        vm.expectRevert(NFTCollection.OnlyOwner.selector);
        nft.ownerMint(user1, 10);
    }

    // ========================================
    // Transfer Tests
    // ========================================

    function testTransferFrom() public {
        vm.prank(user1);
        uint256 tokenId = nft.mint{value: MINT_PRICE}();

        vm.prank(user1);
        nft.transferFrom(user1, user2, tokenId);

        assertEq(nft.ownerOf(tokenId), user2);
        assertEq(nft.balanceOf(user1), 0);
        assertEq(nft.balanceOf(user2), 1);
    }

    function testTransferFromNotOwner() public {
        vm.prank(user1);
        uint256 tokenId = nft.mint{value: MINT_PRICE}();

        vm.prank(user2);
        vm.expectRevert(NFTCollection.NotOwnerOrApproved.selector);
        nft.transferFrom(user1, user2, tokenId);
    }

    function testApprove() public {
        vm.prank(user1);
        uint256 tokenId = nft.mint{value: MINT_PRICE}();

        vm.prank(user1);
        nft.approve(user2, tokenId);

        assertEq(nft.getApproved(tokenId), user2);

        // user2 can now transfer
        vm.prank(user2);
        nft.transferFrom(user1, user2, tokenId);

        assertEq(nft.ownerOf(tokenId), user2);
    }

    function testSetApprovalForAll() public {
        vm.prank(user1);
        nft.setApprovalForAll(user2, true);

        assertTrue(nft.isApprovedForAll(user1, user2));
    }

    // ========================================
    // URI Tests
    // ========================================

    function testTokenURIUnrevealed() public {
        vm.prank(user1);
        uint256 tokenId = nft.mint{value: MINT_PRICE}();

        string memory uri = nft.tokenURI(tokenId);
        assertEq(uri, UNREVEALED_URI);
    }

    function testReveal() public {
        vm.prank(user1);
        uint256 tokenId = nft.mint{value: MINT_PRICE}();

        string memory baseURI = "ipfs://revealed/";
        nft.reveal(baseURI);

        assertTrue(nft.revealed());

        string memory uri = nft.tokenURI(tokenId);
        assertEq(uri, string(abi.encodePacked(baseURI, "1.json")));
    }

    function testRevealOnlyOwner() public {
        vm.prank(user1);
        vm.expectRevert(NFTCollection.OnlyOwner.selector);
        nft.reveal("ipfs://test/");
    }

    // ========================================
    // Whitelist Tests
    // ========================================

    function testWhitelistMinting() public {
        // Enable whitelist
        nft.setWhitelistEnabled(true);

        // user1 is not whitelisted
        vm.prank(user1);
        vm.expectRevert(NFTCollection.NotWhitelisted.selector);
        nft.mint{value: MINT_PRICE}();

        // Add user1 to whitelist
        address[] memory addresses = new address[](1);
        addresses[0] = user1;
        nft.addToWhitelist(addresses);

        assertTrue(nft.whitelist(user1));

        // Now user1 can mint
        vm.prank(user1);
        uint256 tokenId = nft.mint{value: MINT_PRICE}();
        assertEq(nft.ownerOf(tokenId), user1);
    }

    function testRemoveFromWhitelist() public {
        address[] memory addresses = new address[](1);
        addresses[0] = user1;

        nft.addToWhitelist(addresses);
        assertTrue(nft.whitelist(user1));

        nft.removeFromWhitelist(addresses);
        assertFalse(nft.whitelist(user1));
    }

    // ========================================
    // Pause Tests
    // ========================================

    function testPause() public {
        nft.pause();
        assertTrue(nft.paused());

        vm.prank(user1);
        vm.expectRevert(NFTCollection.ContractPaused.selector);
        nft.mint{value: MINT_PRICE}();
    }

    function testUnpause() public {
        nft.pause();
        nft.unpause();
        assertFalse(nft.paused());

        vm.prank(user1);
        nft.mint{value: MINT_PRICE}();
    }

    // ========================================
    // Royalty Tests
    // ========================================

    function testRoyaltyInfo() public {
        uint256 salePrice = 1 ether;
        (address receiver, uint256 royaltyAmount) = nft.royaltyInfo(1, salePrice);

        assertEq(receiver, owner);
        assertEq(royaltyAmount, salePrice * 250 / 10000); // 2.5%
    }

    function testSetRoyalty() public {
        address newReceiver = user1;
        uint96 newBasisPoints = 500; // 5%

        nft.setRoyalty(newReceiver, newBasisPoints);

        assertEq(nft.royaltyReceiver(), newReceiver);
        assertEq(nft.royaltyBasisPoints(), newBasisPoints);

        (address receiver, uint256 royaltyAmount) = nft.royaltyInfo(1, 1 ether);
        assertEq(receiver, newReceiver);
        assertEq(royaltyAmount, 0.05 ether);
    }

    // ========================================
    // Admin Tests
    // ========================================

    function testSetMintPrice() public {
        uint256 newPrice = 0.2 ether;
        nft.setMintPrice(newPrice);
        assertEq(nft.mintPrice(), newPrice);
    }

    function testWithdraw() public {
        // Mint some NFTs
        vm.prank(user1);
        nft.mint{value: MINT_PRICE}();

        uint256 contractBalance = address(nft).balance;
        uint256 ownerBalanceBefore = owner.balance;

        nft.withdraw();

        assertEq(address(nft).balance, 0);
        assertEq(owner.balance, ownerBalanceBefore + contractBalance);
    }

    function testTransferOwnership() public {
        nft.transferOwnership(user1);
        assertEq(nft.owner(), user1);
    }

    // ========================================
    // ERC-165 Tests
    // ========================================

    function testSupportsInterface() public {
        assertTrue(nft.supportsInterface(0x01ffc9a7)); // ERC-165
        assertTrue(nft.supportsInterface(0x80ac58cd)); // ERC-721
        assertTrue(nft.supportsInterface(0x2a55205a)); // EIP-2981
    }

    // ========================================
    // Integration Test
    // ========================================

    function testCompleteWorkflow() public {
        // 1. Owner mints to user1
        nft.ownerMint(user1, 5);

        // 2. user1 mints
        vm.prank(user1);
        nft.mint{value: MINT_PRICE}();

        assertEq(nft.balanceOf(user1), 6);

        // 3. Reveal
        nft.reveal("ipfs://revealed/");
        assertTrue(nft.revealed());

        // 4. user1 transfers to user2
        vm.prank(user1);
        nft.transferFrom(user1, user2, 1);

        assertEq(nft.ownerOf(1), user2);
        assertEq(nft.balanceOf(user1), 5);
        assertEq(nft.balanceOf(user2), 1);

        // 5. Withdraw funds
        uint256 contractBalance = address(nft).balance;
        nft.withdraw();
        assertEq(address(nft).balance, 0);
    }
}
