// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "../src/DEX.sol";

contract DeployDEX is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");

        vm.startBroadcast(deployerPrivateKey);

        // Deploy DEX (factory + router)
        DEX dex = new DEX();

        console.log("DEX deployed at:", address(dex));
        console.log("Owner:", dex.owner());

        vm.stopBroadcast();
    }
}
