// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "../src/DEX.sol";
import "../src/Pair.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

// Mock ERC20 for testing
contract MockERC20 is ERC20 {
    constructor(string memory name, string memory symbol) ERC20(name, symbol) {
        _mint(msg.sender, 1_000_000 * 10 ** 18);
    }

    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

contract DEXTest is Test {
    DEX public dex;
    MockERC20 public tokenA;
    MockERC20 public tokenB;
    MockERC20 public tokenC;

    address public user1 = address(0x1);
    address public user2 = address(0x2);
    uint256 public constant INITIAL_BALANCE = 10_000 * 10 ** 18;

    event PairCreated(address indexed token0, address indexed token1, address pair, uint256);
    event LiquidityAdded(address indexed pair, address indexed provider, uint256, uint256, uint256);

    function setUp() public {
        // Deploy DEX
        dex = new DEX();

        // Deploy tokens
        tokenA = new MockERC20("Token A", "TKA");
        tokenB = new MockERC20("Token B", "TKB");
        tokenC = new MockERC20("Token C", "TKC");

        // Setup users
        tokenA.transfer(user1, INITIAL_BALANCE);
        tokenB.transfer(user1, INITIAL_BALANCE);
        tokenC.transfer(user1, INITIAL_BALANCE);

        tokenA.transfer(user2, INITIAL_BALANCE);
        tokenB.transfer(user2, INITIAL_BALANCE);
    }

    // ==================== Pair Creation Tests ====================

    function testCreatePair() public {
        address pair = dex.createPair(address(tokenA), address(tokenB));

        assertEq(dex.getPair(address(tokenA), address(tokenB)), pair);
        assertEq(dex.getPair(address(tokenB), address(tokenA)), pair);
        assertEq(dex.allPairsLength(), 1);
    }

    function testCreatePairRevertsOnIdenticalTokens() public {
        vm.expectRevert(DEX.IdenticalAddresses.selector);
        dex.createPair(address(tokenA), address(tokenA));
    }

    function testCreatePairRevertsOnZeroAddress() public {
        vm.expectRevert(DEX.ZeroAddress.selector);
        dex.createPair(address(0), address(tokenB));
    }

    function testCreatePairRevertsIfExists() public {
        dex.createPair(address(tokenA), address(tokenB));

        vm.expectRevert(DEX.PairExists.selector);
        dex.createPair(address(tokenA), address(tokenB));
    }

    // ==================== Liquidity Tests ====================

    function testAddLiquidityCreatesNewPair() public {
        vm.startPrank(user1);

        tokenA.approve(address(dex), INITIAL_BALANCE);
        tokenB.approve(address(dex), INITIAL_BALANCE);

        uint256 amountA = 1000 * 10 ** 18;
        uint256 amountB = 2000 * 10 ** 18;

        (uint256 actualA, uint256 actualB, uint256 liquidity) = dex.addLiquidity(
            address(tokenA),
            address(tokenB),
            amountA,
            amountB,
            0,
            0,
            user1,
            block.timestamp + 100
        );

        vm.stopPrank();

        assertEq(actualA, amountA);
        assertEq(actualB, amountB);
        assertGt(liquidity, 0);
        assertEq(dex.allPairsLength(), 1);
    }

    function testAddLiquidityToExistingPair() public {
        // First liquidity
        vm.startPrank(user1);
        tokenA.approve(address(dex), INITIAL_BALANCE);
        tokenB.approve(address(dex), INITIAL_BALANCE);

        dex.addLiquidity(
            address(tokenA),
            address(tokenB),
            1000 * 10 ** 18,
            2000 * 10 ** 18,
            0,
            0,
            user1,
            block.timestamp + 100
        );
        vm.stopPrank();

        // Second liquidity
        vm.startPrank(user2);
        tokenA.approve(address(dex), INITIAL_BALANCE);
        tokenB.approve(address(dex), INITIAL_BALANCE);

        (,, uint256 liquidity2) = dex.addLiquidity(
            address(tokenA),
            address(tokenB),
            500 * 10 ** 18,
            1000 * 10 ** 18,
            0,
            0,
            user2,
            block.timestamp + 100
        );
        vm.stopPrank();

        assertGt(liquidity2, 0);
    }

    function testRemoveLiquidity() public {
        // Add liquidity
        vm.startPrank(user1);
        tokenA.approve(address(dex), INITIAL_BALANCE);
        tokenB.approve(address(dex), INITIAL_BALANCE);

        (,, uint256 liquidity) = dex.addLiquidity(
            address(tokenA),
            address(tokenB),
            1000 * 10 ** 18,
            2000 * 10 ** 18,
            0,
            0,
            user1,
            block.timestamp + 100
        );

        address pair = dex.getPair(address(tokenA), address(tokenB));

        // Approve and remove liquidity
        Pair(pair).approve(address(dex), liquidity);

        uint256 balanceABefore = tokenA.balanceOf(user1);
        uint256 balanceBBefore = tokenB.balanceOf(user1);

        (uint256 amountA, uint256 amountB) = dex.removeLiquidity(
            address(tokenA),
            address(tokenB),
            liquidity,
            0,
            0,
            user1,
            block.timestamp + 100
        );

        vm.stopPrank();

        assertGt(amountA, 0);
        assertGt(amountB, 0);
        assertEq(tokenA.balanceOf(user1) - balanceABefore, amountA);
        assertEq(tokenB.balanceOf(user1) - balanceBBefore, amountB);
    }

    // ==================== Swap Tests ====================

    function testSwapExactTokensForTokens() public {
        // Setup: Add liquidity
        vm.startPrank(user1);
        tokenA.approve(address(dex), INITIAL_BALANCE);
        tokenB.approve(address(dex), INITIAL_BALANCE);

        dex.addLiquidity(
            address(tokenA),
            address(tokenB),
            10000 * 10 ** 18,
            20000 * 10 ** 18,
            0,
            0,
            user1,
            block.timestamp + 100
        );
        vm.stopPrank();

        // Swap
        vm.startPrank(user2);
        uint256 amountIn = 100 * 10 ** 18;
        tokenA.approve(address(dex), amountIn);

        address[] memory path = new address[](2);
        path[0] = address(tokenA);
        path[1] = address(tokenB);

        uint256 balanceBBefore = tokenB.balanceOf(user2);

        uint256[] memory amounts = dex.swapExactTokensForTokens(
            amountIn,
            0,
            path,
            user2,
            block.timestamp + 100
        );

        vm.stopPrank();

        assertEq(amounts[0], amountIn);
        assertGt(amounts[1], 0);
        assertEq(tokenB.balanceOf(user2) - balanceBBefore, amounts[1]);
    }

    function testSwapTokensForExactTokens() public {
        // Setup: Add liquidity
        vm.startPrank(user1);
        tokenA.approve(address(dex), INITIAL_BALANCE);
        tokenB.approve(address(dex), INITIAL_BALANCE);

        dex.addLiquidity(
            address(tokenA),
            address(tokenB),
            10000 * 10 ** 18,
            20000 * 10 ** 18,
            0,
            0,
            user1,
            block.timestamp + 100
        );
        vm.stopPrank();

        // Swap
        vm.startPrank(user2);
        uint256 amountOut = 100 * 10 ** 18;
        tokenA.approve(address(dex), INITIAL_BALANCE);

        address[] memory path = new address[](2);
        path[0] = address(tokenA);
        path[1] = address(tokenB);

        uint256 balanceBBefore = tokenB.balanceOf(user2);

        uint256[] memory amounts = dex.swapTokensForExactTokens(
            amountOut,
            INITIAL_BALANCE,
            path,
            user2,
            block.timestamp + 100
        );

        vm.stopPrank();

        assertGt(amounts[0], 0);
        assertEq(amounts[1], amountOut);
        assertEq(tokenB.balanceOf(user2) - balanceBBefore, amountOut);
    }

    function testMultiHopSwap() public {
        // Setup: Create A-B and B-C pairs
        vm.startPrank(user1);
        tokenA.approve(address(dex), INITIAL_BALANCE);
        tokenB.approve(address(dex), INITIAL_BALANCE);
        tokenC.approve(address(dex), INITIAL_BALANCE);

        // Add A-B liquidity
        dex.addLiquidity(
            address(tokenA),
            address(tokenB),
            10000 * 10 ** 18,
            10000 * 10 ** 18,
            0,
            0,
            user1,
            block.timestamp + 100
        );

        // Add B-C liquidity
        dex.addLiquidity(
            address(tokenB),
            address(tokenC),
            10000 * 10 ** 18,
            10000 * 10 ** 18,
            0,
            0,
            user1,
            block.timestamp + 100
        );
        vm.stopPrank();

        // Multi-hop swap: A -> B -> C
        vm.startPrank(user2);
        uint256 amountIn = 100 * 10 ** 18;
        tokenA.approve(address(dex), amountIn);

        address[] memory path = new address[](3);
        path[0] = address(tokenA);
        path[1] = address(tokenB);
        path[2] = address(tokenC);

        uint256 balanceCBefore = tokenC.balanceOf(user2);

        uint256[] memory amounts = dex.swapExactTokensForTokens(
            amountIn,
            0,
            path,
            user2,
            block.timestamp + 100
        );

        vm.stopPrank();

        assertEq(amounts[0], amountIn);
        assertGt(amounts[2], 0);
        assertEq(tokenC.balanceOf(user2) - balanceCBefore, amounts[2]);
    }

    // ==================== View Function Tests ====================

    function testGetAmountsOut() public {
        // Setup liquidity
        vm.startPrank(user1);
        tokenA.approve(address(dex), INITIAL_BALANCE);
        tokenB.approve(address(dex), INITIAL_BALANCE);

        dex.addLiquidity(
            address(tokenA),
            address(tokenB),
            10000 * 10 ** 18,
            20000 * 10 ** 18,
            0,
            0,
            user1,
            block.timestamp + 100
        );
        vm.stopPrank();

        address[] memory path = new address[](2);
        path[0] = address(tokenA);
        path[1] = address(tokenB);

        uint256[] memory amounts = dex.getAmountsOut(100 * 10 ** 18, path);

        assertEq(amounts[0], 100 * 10 ** 18);
        assertGt(amounts[1], 0);
        // Verify output is less than input due to slippage
        assertLt(amounts[1], 200 * 10 ** 18);
    }

    function testGetAmountsIn() public {
        // Setup liquidity
        vm.startPrank(user1);
        tokenA.approve(address(dex), INITIAL_BALANCE);
        tokenB.approve(address(dex), INITIAL_BALANCE);

        dex.addLiquidity(
            address(tokenA),
            address(tokenB),
            10000 * 10 ** 18,
            20000 * 10 ** 18,
            0,
            0,
            user1,
            block.timestamp + 100
        );
        vm.stopPrank();

        address[] memory path = new address[](2);
        path[0] = address(tokenA);
        path[1] = address(tokenB);

        uint256[] memory amounts = dex.getAmountsIn(100 * 10 ** 18, path);

        assertGt(amounts[0], 0);
        assertEq(amounts[1], 100 * 10 ** 18);
    }

    function testQuote() public {
        uint256 amountA = 100 * 10 ** 18;
        uint256 reserveA = 1000 * 10 ** 18;
        uint256 reserveB = 2000 * 10 ** 18;

        uint256 amountB = dex.quote(amountA, reserveA, reserveB);

        assertEq(amountB, 200 * 10 ** 18);
    }

    // ==================== Error Tests ====================

    function testSwapRevertsOnExpiredDeadline() public {
        vm.startPrank(user1);
        address[] memory path = new address[](2);
        path[0] = address(tokenA);
        path[1] = address(tokenB);

        vm.expectRevert(DEX.Expired.selector);
        dex.swapExactTokensForTokens(100, 0, path, user1, block.timestamp - 1);
        vm.stopPrank();
    }

    function testSwapRevertsOnNonexistentPair() public {
        vm.startPrank(user2);
        tokenA.approve(address(dex), 100);

        address[] memory path = new address[](2);
        path[0] = address(tokenA);
        path[1] = address(tokenB);

        vm.expectRevert(DEX.PairDoesNotExist.selector);
        dex.swapExactTokensForTokens(100, 0, path, user2, block.timestamp + 100);
        vm.stopPrank();
    }

    // ==================== Integration Tests ====================

    function testFullWorkflow() public {
        // 1. Create pair and add liquidity
        vm.startPrank(user1);
        tokenA.approve(address(dex), INITIAL_BALANCE);
        tokenB.approve(address(dex), INITIAL_BALANCE);

        (,, uint256 liquidity) = dex.addLiquidity(
            address(tokenA),
            address(tokenB),
            1000 * 10 ** 18,
            2000 * 10 ** 18,
            0,
            0,
            user1,
            block.timestamp + 100
        );
        vm.stopPrank();

        assertGt(liquidity, 0);

        // 2. User2 swaps
        vm.startPrank(user2);
        uint256 amountIn = 100 * 10 ** 18;
        tokenA.approve(address(dex), amountIn);

        address[] memory path = new address[](2);
        path[0] = address(tokenA);
        path[1] = address(tokenB);

        uint256[] memory amounts = dex.swapExactTokensForTokens(
            amountIn,
            0,
            path,
            user2,
            block.timestamp + 100
        );
        vm.stopPrank();

        assertGt(amounts[1], 0);

        // 3. User1 removes liquidity
        vm.startPrank(user1);
        address pair = dex.getPair(address(tokenA), address(tokenB));
        Pair(pair).approve(address(dex), liquidity);

        (uint256 amountA, uint256 amountB) = dex.removeLiquidity(
            address(tokenA),
            address(tokenB),
            liquidity,
            0,
            0,
            user1,
            block.timestamp + 100
        );
        vm.stopPrank();

        // Should get back more than initial due to trading fees
        assertGt(amountA, 1000 * 10 ** 18);
    }
}
