// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./Pair.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title DEX
 * @notice Factory and Router for creating and interacting with liquidity pairs
 * @dev Uniswap V2-style factory + router combined
 */
contract DEX is Ownable {
    // ==================== State Variables ====================

    mapping(address => mapping(address => address)) public getPair;
    address[] public allPairs;

    // Fee recipient (for protocol fees if implemented)
    address public feeTo;

    // ==================== Events ====================

    event PairCreated(
        address indexed token0,
        address indexed token1,
        address pair,
        uint256 pairCount
    );
    event LiquidityAdded(
        address indexed pair,
        address indexed provider,
        uint256 amount0,
        uint256 amount1,
        uint256 liquidity
    );
    event LiquidityRemoved(
        address indexed pair,
        address indexed provider,
        uint256 amount0,
        uint256 amount1,
        uint256 liquidity
    );
    event TokensSwapped(
        address indexed pair,
        address indexed trader,
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        uint256 amountOut
    );

    // ==================== Errors ====================

    error IdenticalAddresses();
    error ZeroAddress();
    error PairExists();
    error PairDoesNotExist();
    error InsufficientAmount();
    error InsufficientLiquidity();
    error InsufficientOutputAmount();
    error ExcessiveInputAmount();
    error Expired();
    error TransferFailed();

    // ==================== Constructor ====================

    constructor() Ownable(msg.sender) {}

    // ==================== Factory Functions ====================

    /**
     * @notice Get total number of pairs
     */
    function allPairsLength() external view returns (uint256) {
        return allPairs.length;
    }

    /**
     * @notice Create a new pair
     * @param tokenA First token address
     * @param tokenB Second token address
     * @return pair Address of created pair
     */
    function createPair(address tokenA, address tokenB) external returns (address pair) {
        if (tokenA == tokenB) revert IdenticalAddresses();

        // Sort tokens
        (address token0, address token1) = tokenA < tokenB ? (tokenA, tokenB) : (tokenB, tokenA);

        if (token0 == address(0)) revert ZeroAddress();
        if (getPair[token0][token1] != address(0)) revert PairExists();

        // Create pair
        pair = address(new Pair(token0, token1));

        // Store pair
        getPair[token0][token1] = pair;
        getPair[token1][token0] = pair; // Bidirectional mapping
        allPairs.push(pair);

        emit PairCreated(token0, token1, pair, allPairs.length);
    }

    // ==================== Router Functions ====================

    /**
     * @notice Add liquidity to a pair
     * @param tokenA First token address
     * @param tokenB Second token address
     * @param amountADesired Desired amount of tokenA
     * @param amountBDesired Desired amount of tokenB
     * @param amountAMin Minimum amount of tokenA
     * @param amountBMin Minimum amount of tokenB
     * @param to Address to receive LP tokens
     * @param deadline Transaction deadline
     * @return amountA Actual amount of tokenA added
     * @return amountB Actual amount of tokenB added
     * @return liquidity Amount of LP tokens received
     */
    function addLiquidity(
        address tokenA,
        address tokenB,
        uint256 amountADesired,
        uint256 amountBDesired,
        uint256 amountAMin,
        uint256 amountBMin,
        address to,
        uint256 deadline
    ) external ensure(deadline) returns (uint256 amountA, uint256 amountB, uint256 liquidity) {
        // Get or create pair
        address pair = getPair[tokenA][tokenB];
        if (pair == address(0)) {
            pair = this.createPair(tokenA, tokenB);
        }

        // Calculate optimal amounts
        (amountA, amountB) = _calculateLiquidityAmounts(
            tokenA,
            tokenB,
            amountADesired,
            amountBDesired,
            amountAMin,
            amountBMin
        );

        // Transfer tokens to pair
        _safeTransferFrom(tokenA, msg.sender, pair, amountA);
        _safeTransferFrom(tokenB, msg.sender, pair, amountB);

        // Mint LP tokens
        liquidity = Pair(pair).mint(to);

        emit LiquidityAdded(pair, msg.sender, amountA, amountB, liquidity);
    }

    /**
     * @notice Remove liquidity from a pair
     * @param tokenA First token address
     * @param tokenB Second token address
     * @param liquidity Amount of LP tokens to burn
     * @param amountAMin Minimum amount of tokenA to receive
     * @param amountBMin Minimum amount of tokenB to receive
     * @param to Address to receive tokens
     * @param deadline Transaction deadline
     * @return amountA Amount of tokenA received
     * @return amountB Amount of tokenB received
     */
    function removeLiquidity(
        address tokenA,
        address tokenB,
        uint256 liquidity,
        uint256 amountAMin,
        uint256 amountBMin,
        address to,
        uint256 deadline
    ) external ensure(deadline) returns (uint256 amountA, uint256 amountB) {
        address pair = getPair[tokenA][tokenB];
        if (pair == address(0)) revert PairDoesNotExist();

        // Transfer LP tokens to pair
        IERC20(pair).transferFrom(msg.sender, pair, liquidity);

        // Burn LP tokens and receive tokens
        (uint256 amount0, uint256 amount1) = Pair(pair).burn(to);

        // Sort amounts back to A/B order
        (address token0,) = tokenA < tokenB ? (tokenA, tokenB) : (tokenB, tokenA);
        (amountA, amountB) = tokenA == token0 ? (amount0, amount1) : (amount1, amount0);

        if (amountA < amountAMin) revert InsufficientAmount();
        if (amountB < amountBMin) revert InsufficientAmount();

        emit LiquidityRemoved(pair, msg.sender, amountA, amountB, liquidity);
    }

    /**
     * @notice Swap exact tokens for tokens
     * @param amountIn Amount of input tokens
     * @param amountOutMin Minimum amount of output tokens
     * @param path Array of token addresses (swap path)
     * @param to Address to receive output tokens
     * @param deadline Transaction deadline
     * @return amounts Array of amounts for each swap in path
     */
    function swapExactTokensForTokens(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external ensure(deadline) returns (uint256[] memory amounts) {
        amounts = getAmountsOut(amountIn, path);
        if (amounts[amounts.length - 1] < amountOutMin) {
            revert InsufficientOutputAmount();
        }

        // Transfer input tokens to first pair
        address firstPair = _getPairAddress(path[0], path[1]);
        _safeTransferFrom(path[0], msg.sender, firstPair, amounts[0]);

        // Execute swaps
        _swap(amounts, path, to);

        emit TokensSwapped(
            firstPair,
            msg.sender,
            path[0],
            path[path.length - 1],
            amountIn,
            amounts[amounts.length - 1]
        );
    }

    /**
     * @notice Swap tokens for exact tokens
     * @param amountOut Exact amount of output tokens desired
     * @param amountInMax Maximum amount of input tokens
     * @param path Array of token addresses (swap path)
     * @param to Address to receive output tokens
     * @param deadline Transaction deadline
     * @return amounts Array of amounts for each swap in path
     */
    function swapTokensForExactTokens(
        uint256 amountOut,
        uint256 amountInMax,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external ensure(deadline) returns (uint256[] memory amounts) {
        amounts = getAmountsIn(amountOut, path);
        if (amounts[0] > amountInMax) revert ExcessiveInputAmount();

        // Transfer input tokens to first pair
        address firstPair = _getPairAddress(path[0], path[1]);
        _safeTransferFrom(path[0], msg.sender, firstPair, amounts[0]);

        // Execute swaps
        _swap(amounts, path, to);

        emit TokensSwapped(
            firstPair,
            msg.sender,
            path[0],
            path[path.length - 1],
            amounts[0],
            amountOut
        );
    }

    // ==================== View Functions ====================

    /**
     * @notice Get amounts out for a swap path
     * @param amountIn Input amount
     * @param path Swap path
     * @return amounts Array of output amounts
     */
    function getAmountsOut(uint256 amountIn, address[] memory path)
        public
        view
        returns (uint256[] memory amounts)
    {
        if (path.length < 2) revert();
        amounts = new uint256[](path.length);
        amounts[0] = amountIn;

        for (uint256 i = 0; i < path.length - 1; i++) {
            address pair = getPair[path[i]][path[i + 1]];
            if (pair == address(0)) revert PairDoesNotExist();

            (uint112 reserve0, uint112 reserve1,) = Pair(pair).getReserves();
            (uint112 reserveIn, uint112 reserveOut) = path[i] < path[i + 1]
                ? (reserve0, reserve1)
                : (reserve1, reserve0);

            amounts[i + 1] = Pair(pair).getAmountOut(amounts[i], reserveIn, reserveOut);
        }
    }

    /**
     * @notice Get amounts in for a swap path
     * @param amountOut Desired output amount
     * @param path Swap path
     * @return amounts Array of input amounts
     */
    function getAmountsIn(uint256 amountOut, address[] memory path)
        public
        view
        returns (uint256[] memory amounts)
    {
        if (path.length < 2) revert();
        amounts = new uint256[](path.length);
        amounts[amounts.length - 1] = amountOut;

        for (uint256 i = path.length - 1; i > 0; i--) {
            address pair = getPair[path[i - 1]][path[i]];
            if (pair == address(0)) revert PairDoesNotExist();

            (uint112 reserve0, uint112 reserve1,) = Pair(pair).getReserves();
            (uint112 reserveIn, uint112 reserveOut) = path[i - 1] < path[i]
                ? (reserve0, reserve1)
                : (reserve1, reserve0);

            amounts[i - 1] = _getAmountIn(amounts[i], reserveIn, reserveOut);
        }
    }

    /**
     * @notice Get quote for adding liquidity
     * @param amountA Amount of tokenA
     * @param reserveA Reserve of tokenA
     * @param reserveB Reserve of tokenB
     * @return amountB Required amount of tokenB
     */
    function quote(uint256 amountA, uint256 reserveA, uint256 reserveB)
        public
        pure
        returns (uint256 amountB)
    {
        if (amountA == 0) revert InsufficientAmount();
        if (reserveA == 0 || reserveB == 0) revert InsufficientLiquidity();
        amountB = (amountA * reserveB) / reserveA;
    }

    // ==================== Internal Functions ====================

    /**
     * @notice Calculate optimal liquidity amounts
     */
    function _calculateLiquidityAmounts(
        address tokenA,
        address tokenB,
        uint256 amountADesired,
        uint256 amountBDesired,
        uint256 amountAMin,
        uint256 amountBMin
    ) internal view returns (uint256 amountA, uint256 amountB) {
        address pair = getPair[tokenA][tokenB];
        (uint112 reserve0, uint112 reserve1,) = Pair(pair).getReserves();
        (address token0,) = tokenA < tokenB ? (tokenA, tokenB) : (tokenB, tokenA);
        (uint112 reserveA, uint112 reserveB) = tokenA == token0
            ? (reserve0, reserve1)
            : (reserve1, reserve0);

        if (reserveA == 0 && reserveB == 0) {
            (amountA, amountB) = (amountADesired, amountBDesired);
        } else {
            uint256 amountBOptimal = quote(amountADesired, reserveA, reserveB);
            if (amountBOptimal <= amountBDesired) {
                if (amountBOptimal < amountBMin) revert InsufficientAmount();
                (amountA, amountB) = (amountADesired, amountBOptimal);
            } else {
                uint256 amountAOptimal = quote(amountBDesired, reserveB, reserveA);
                assert(amountAOptimal <= amountADesired);
                if (amountAOptimal < amountAMin) revert InsufficientAmount();
                (amountA, amountB) = (amountAOptimal, amountBDesired);
            }
        }
    }

    /**
     * @notice Execute swap along a path
     */
    function _swap(uint256[] memory amounts, address[] memory path, address to) internal {
        for (uint256 i = 0; i < path.length - 1; i++) {
            (address input, address output) = (path[i], path[i + 1]);
            address pair = getPair[input][output];

            (uint256 amount0Out, uint256 amount1Out) = input < output
                ? (uint256(0), amounts[i + 1])
                : (amounts[i + 1], uint256(0));

            address _to = i < path.length - 2 ? getPair[output][path[i + 2]] : to;
            Pair(pair).swap(amount0Out, amount1Out, _to);
        }
    }

    /**
     * @notice Get pair address (reverts if doesn't exist)
     */
    function _getPairAddress(address tokenA, address tokenB) internal view returns (address pair) {
        pair = getPair[tokenA][tokenB];
        if (pair == address(0)) revert PairDoesNotExist();
    }

    /**
     * @notice Calculate amount in for exact amount out
     */
    function _getAmountIn(uint256 amountOut, uint256 reserveIn, uint256 reserveOut)
        internal
        pure
        returns (uint256 amountIn)
    {
        if (amountOut == 0) revert InsufficientOutputAmount();
        if (reserveIn == 0 || reserveOut == 0) revert InsufficientLiquidity();

        uint256 numerator = reserveIn * amountOut * 1000;
        uint256 denominator = (reserveOut - amountOut) * 997;
        amountIn = (numerator / denominator) + 1;
    }

    /**
     * @notice Safe transfer from
     */
    function _safeTransferFrom(address token, address from, address to, uint256 value) internal {
        bool success = IERC20(token).transferFrom(from, to, value);
        if (!success) revert TransferFailed();
    }

    // ==================== Modifiers ====================

    modifier ensure(uint256 deadline) {
        if (block.timestamp > deadline) revert Expired();
        _;
    }

    // ==================== Admin Functions ====================

    /**
     * @notice Set fee recipient
     */
    function setFeeTo(address _feeTo) external onlyOwner {
        feeTo = _feeTo;
    }
}
