// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "../src/BasicERC20.sol";

/**
 * @title BasicERC20Test
 * @dev Comprehensive tests สำหรับ BasicERC20 contract
 */
contract BasicERC20Test is Test {
    BasicERC20 public token;

    address public owner;
    address public user1;
    address public user2;

    uint256 constant INITIAL_SUPPLY = 1_000_000 * 10**18; // 1 million tokens

    // Events for testing
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Mint(address indexed to, uint256 amount);
    event Burn(address indexed from, uint256 amount);
    event Paused(address account);
    event Unpaused(address account);

    function setUp() public {
        owner = address(this);
        user1 = makeAddr("user1");
        user2 = makeAddr("user2");

        token = new BasicERC20("My Token", "MTK", INITIAL_SUPPLY);
    }

    // ========================================
    // Constructor Tests
    // ========================================

    function testConstructor() public {
        assertEq(token.name(), "My Token");
        assertEq(token.symbol(), "MTK");
        assertEq(token.decimals(), 18);
        assertEq(token.totalSupply(), INITIAL_SUPPLY);
        assertEq(token.balanceOf(owner), INITIAL_SUPPLY);
        assertEq(token.owner(), owner);
        assertEq(token.paused(), false);
    }

    function testConstructorWithZeroSupply() public {
        BasicERC20 newToken = new BasicERC20("Zero Token", "ZTK", 0);
        assertEq(newToken.totalSupply(), 0);
        assertEq(newToken.balanceOf(owner), 0);
    }

    // ========================================
    // Transfer Tests
    // ========================================

    function testTransfer() public {
        uint256 amount = 100 * 10**18;

        vm.expectEmit(true, true, false, true);
        emit Transfer(owner, user1, amount);

        bool success = token.transfer(user1, amount);

        assertTrue(success);
        assertEq(token.balanceOf(owner), INITIAL_SUPPLY - amount);
        assertEq(token.balanceOf(user1), amount);
    }

    function testTransferInsufficientBalance() public {
        uint256 amount = INITIAL_SUPPLY + 1;

        vm.expectRevert(
            abi.encodeWithSelector(
                BasicERC20.ERC20InsufficientBalance.selector,
                owner,
                INITIAL_SUPPLY,
                amount
            )
        );
        token.transfer(user1, amount);
    }

    function testTransferToZeroAddress() public {
        vm.expectRevert(
            abi.encodeWithSelector(
                BasicERC20.ERC20InvalidReceiver.selector,
                address(0)
            )
        );
        token.transfer(address(0), 100);
    }

    function testTransferFuzz(uint256 amount) public {
        // Bound amount to available balance
        amount = bound(amount, 0, INITIAL_SUPPLY);

        token.transfer(user1, amount);

        assertEq(token.balanceOf(user1), amount);
        assertEq(token.balanceOf(owner), INITIAL_SUPPLY - amount);
    }

    // ========================================
    // Approve & TransferFrom Tests
    // ========================================

    function testApprove() public {
        uint256 amount = 100 * 10**18;

        vm.expectEmit(true, true, false, true);
        emit Approval(owner, user1, amount);

        bool success = token.approve(user1, amount);

        assertTrue(success);
        assertEq(token.allowance(owner, user1), amount);
    }

    function testApproveToZeroAddress() public {
        vm.expectRevert(
            abi.encodeWithSelector(
                BasicERC20.ERC20InvalidSpender.selector,
                address(0)
            )
        );
        token.approve(address(0), 100);
    }

    function testTransferFrom() public {
        uint256 amount = 100 * 10**18;

        // Owner approves user1 to spend
        token.approve(user1, amount);

        // user1 transfers from owner to user2
        vm.prank(user1);
        vm.expectEmit(true, true, false, true);
        emit Transfer(owner, user2, amount);

        bool success = token.transferFrom(owner, user2, amount);

        assertTrue(success);
        assertEq(token.balanceOf(user2), amount);
        assertEq(token.balanceOf(owner), INITIAL_SUPPLY - amount);
        assertEq(token.allowance(owner, user1), 0);
    }

    function testTransferFromInsufficientAllowance() public {
        uint256 approvedAmount = 50 * 10**18;
        uint256 transferAmount = 100 * 10**18;

        token.approve(user1, approvedAmount);

        vm.prank(user1);
        vm.expectRevert(
            abi.encodeWithSelector(
                BasicERC20.ERC20InsufficientAllowance.selector,
                user1,
                approvedAmount,
                transferAmount
            )
        );
        token.transferFrom(owner, user2, transferAmount);
    }

    function testTransferFromWithMaxAllowance() public {
        uint256 amount = 100 * 10**18;

        // Approve max uint256 (infinite approval)
        token.approve(user1, type(uint256).max);

        vm.prank(user1);
        token.transferFrom(owner, user2, amount);

        // Allowance should still be max (not decreased)
        assertEq(token.allowance(owner, user1), type(uint256).max);
    }

    // ========================================
    // Mint Tests
    // ========================================

    function testMint() public {
        uint256 mintAmount = 500 * 10**18;

        vm.expectEmit(true, true, false, true);
        emit Mint(user1, mintAmount);

        token.mint(user1, mintAmount);

        assertEq(token.balanceOf(user1), mintAmount);
        assertEq(token.totalSupply(), INITIAL_SUPPLY + mintAmount);
    }

    function testMintOnlyOwner() public {
        vm.prank(user1);
        vm.expectRevert(
            abi.encodeWithSelector(
                BasicERC20.OwnableUnauthorizedAccount.selector,
                user1
            )
        );
        token.mint(user1, 100);
    }

    function testMintToZeroAddress() public {
        vm.expectRevert(
            abi.encodeWithSelector(
                BasicERC20.ERC20InvalidReceiver.selector,
                address(0)
            )
        );
        token.mint(address(0), 100);
    }

    // ========================================
    // Burn Tests
    // ========================================

    function testBurn() public {
        uint256 burnAmount = 100 * 10**18;

        vm.expectEmit(true, true, false, true);
        emit Burn(owner, burnAmount);

        token.burn(burnAmount);

        assertEq(token.balanceOf(owner), INITIAL_SUPPLY - burnAmount);
        assertEq(token.totalSupply(), INITIAL_SUPPLY - burnAmount);
    }

    function testBurnInsufficientBalance() public {
        vm.prank(user1); // user1 has 0 balance

        vm.expectRevert(
            abi.encodeWithSelector(
                BasicERC20.ERC20InsufficientBalance.selector,
                user1,
                0,
                100
            )
        );
        token.burn(100);
    }

    function testBurnFrom() public {
        uint256 amount = 100 * 10**18;

        // Owner transfers to user1
        token.transfer(user1, amount);

        // user1 approves user2 to burn
        vm.prank(user1);
        token.approve(user2, amount);

        // user2 burns user1's tokens
        vm.prank(user2);
        token.burnFrom(user1, amount);

        assertEq(token.balanceOf(user1), 0);
        assertEq(token.totalSupply(), INITIAL_SUPPLY - amount);
    }

    // ========================================
    // Pause Tests
    // ========================================

    function testPause() public {
        vm.expectEmit(false, false, false, true);
        emit Paused(owner);

        token.pause();

        assertTrue(token.paused());
    }

    function testPauseOnlyOwner() public {
        vm.prank(user1);
        vm.expectRevert(
            abi.encodeWithSelector(
                BasicERC20.OwnableUnauthorizedAccount.selector,
                user1
            )
        );
        token.pause();
    }

    function testUnpause() public {
        token.pause();

        vm.expectEmit(false, false, false, true);
        emit Unpaused(owner);

        token.unpause();

        assertFalse(token.paused());
    }

    function testTransferWhenPaused() public {
        token.pause();

        vm.expectRevert(BasicERC20.EnforcedPause.selector);
        token.transfer(user1, 100);
    }

    function testTransferFromWhenPaused() public {
        token.approve(user1, 100);
        token.pause();

        vm.prank(user1);
        vm.expectRevert(BasicERC20.EnforcedPause.selector);
        token.transferFrom(owner, user2, 100);
    }

    function testMintWhenPaused() public {
        token.pause();

        // Mint should still work when paused
        token.mint(user1, 100);
        assertEq(token.balanceOf(user1), 100);
    }

    // ========================================
    // Ownership Tests
    // ========================================

    function testTransferOwnership() public {
        token.transferOwnership(user1);

        assertEq(token.owner(), user1);
    }

    function testTransferOwnershipOnlyOwner() public {
        vm.prank(user1);
        vm.expectRevert(
            abi.encodeWithSelector(
                BasicERC20.OwnableUnauthorizedAccount.selector,
                user1
            )
        );
        token.transferOwnership(user2);
    }

    function testTransferOwnershipToZeroAddress() public {
        vm.expectRevert(
            abi.encodeWithSelector(
                BasicERC20.OwnableInvalidOwner.selector,
                address(0)
            )
        );
        token.transferOwnership(address(0));
    }

    function testRenounceOwnership() public {
        token.renounceOwnership();

        assertEq(token.owner(), address(0));
    }

    function testOwnershipFunctionsAfterRenounce() public {
        token.renounceOwnership();

        vm.expectRevert(
            abi.encodeWithSelector(
                BasicERC20.OwnableUnauthorizedAccount.selector,
                owner
            )
        );
        token.mint(user1, 100);
    }

    // ========================================
    // Integration Tests
    // ========================================

    function testCompleteWorkflow() public {
        // 1. Initial state
        assertEq(token.balanceOf(owner), INITIAL_SUPPLY);

        // 2. Transfer to user1
        token.transfer(user1, 1000 * 10**18);
        assertEq(token.balanceOf(user1), 1000 * 10**18);

        // 3. user1 approves user2
        vm.prank(user1);
        token.approve(user2, 500 * 10**18);

        // 4. user2 transfers from user1
        vm.prank(user2);
        token.transferFrom(user1, user2, 300 * 10**18);
        assertEq(token.balanceOf(user2), 300 * 10**18);

        // 5. Mint new tokens
        token.mint(user1, 2000 * 10**18);
        assertEq(token.totalSupply(), INITIAL_SUPPLY + 2000 * 10**18);

        // 6. Burn tokens
        vm.prank(user1);
        token.burn(500 * 10**18);

        // 7. Pause and attempt transfer
        token.pause();
        vm.prank(user1);
        vm.expectRevert(BasicERC20.EnforcedPause.selector);
        token.transfer(user2, 100);

        // 8. Unpause and transfer
        token.unpause();
        vm.prank(user1);
        token.transfer(user2, 100 * 10**18);

        // Final assertions
        assertFalse(token.paused());
        assertGt(token.balanceOf(user2), 0);
    }
}
