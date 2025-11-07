// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "../src/BasicERC20.sol";

/**
 * @title DeployBasicERC20
 * @dev Deployment script สำหรับ BasicERC20 token
 *
 * วิธีใช้:
 *
 * 1. Deploy to local network (Anvil):
 *    forge script script/Deploy.s.sol:DeployBasicERC20 \
 *      --rpc-url http://localhost:8545 \
 *      --private-key 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80 \
 *      --broadcast
 *
 * 2. Deploy to testnet (Sepolia):
 *    forge script script/Deploy.s.sol:DeployBasicERC20 \
 *      --rpc-url $SEPOLIA_RPC_URL \
 *      --private-key $PRIVATE_KEY \
 *      --broadcast \
 *      --verify \
 *      --etherscan-api-key $ETHERSCAN_API_KEY
 *
 * 3. Deploy with custom parameters:
 *    forge script script/Deploy.s.sol:DeployBasicERC20 \
 *      --sig "run(string,string,uint256)" "Custom Token" "CTK" 1000000000000000000000000 \
 *      --rpc-url http://localhost:8545 \
 *      --private-key 0x... \
 *      --broadcast
 */
contract DeployBasicERC20 is Script {
    // Default parameters
    string constant DEFAULT_NAME = "My Token";
    string constant DEFAULT_SYMBOL = "MTK";
    uint256 constant DEFAULT_SUPPLY = 1_000_000 * 10**18; // 1 million tokens

    function run() external returns (BasicERC20) {
        return deploy(DEFAULT_NAME, DEFAULT_SYMBOL, DEFAULT_SUPPLY);
    }

    function run(
        string memory name,
        string memory symbol,
        uint256 initialSupply
    ) external returns (BasicERC20) {
        return deploy(name, symbol, initialSupply);
    }

    function deploy(
        string memory name,
        string memory symbol,
        uint256 initialSupply
    ) public returns (BasicERC20) {
        console.log("========================================");
        console.log("Deploying BasicERC20 Token");
        console.log("========================================");
        console.log("Name:", name);
        console.log("Symbol:", symbol);
        console.log("Initial Supply:", initialSupply);
        console.log("Deployer:", msg.sender);
        console.log("");

        vm.startBroadcast();

        BasicERC20 token = new BasicERC20(name, symbol, initialSupply);

        vm.stopBroadcast();

        console.log("========================================");
        console.log("Deployment Successful!");
        console.log("========================================");
        console.log("Token Address:", address(token));
        console.log("Owner:", token.owner());
        console.log("Total Supply:", token.totalSupply());
        console.log("Decimals:", token.decimals());
        console.log("");

        // Verification info
        console.log("========================================");
        console.log("Verification Info");
        console.log("========================================");
        console.log("Constructor Args:");
        console.log("  name:", name);
        console.log("  symbol:", symbol);
        console.log("  initialSupply:", initialSupply);
        console.log("");

        return token;
    }

    // Helper function สำหรับ testnet deployment
    function deployToTestnet() external returns (BasicERC20) {
        require(
            block.chainid != 1,
            "Cannot deploy to mainnet with this function"
        );

        return deploy(DEFAULT_NAME, DEFAULT_SYMBOL, DEFAULT_SUPPLY);
    }

    // Helper function สำหรับ production deployment
    function deployToMainnet(
        string memory name,
        string memory symbol,
        uint256 initialSupply
    ) external returns (BasicERC20) {
        require(
            block.chainid == 1,
            "This function is only for mainnet deployment"
        );

        // Additional checks for mainnet
        require(bytes(name).length > 0, "Name cannot be empty");
        require(bytes(symbol).length > 0, "Symbol cannot be empty");
        require(initialSupply > 0, "Initial supply must be greater than 0");

        console.log("!!! MAINNET DEPLOYMENT !!!");
        console.log("Please double-check all parameters");

        return deploy(name, symbol, initialSupply);
    }
}
