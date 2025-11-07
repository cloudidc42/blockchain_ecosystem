// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "../src/NFTCollection.sol";

contract DeployNFTCollection is Script {
    function run() external returns (NFTCollection) {
        string memory name = "My NFT Collection";
        string memory symbol = "MNFT";
        uint256 maxSupply = 10000;
        uint256 mintPrice = 0.08 ether;
        string memory unrevealedURI = "ipfs://QmUnrevealed/hidden.json";

        return deploy(name, symbol, maxSupply, mintPrice, unrevealedURI);
    }

    function deploy(
        string memory name,
        string memory symbol,
        uint256 maxSupply,
        uint256 mintPrice,
        string memory unrevealedURI
    ) public returns (NFTCollection) {
        console.log("Deploying NFTCollection...");
        console.log("Name:", name);
        console.log("Symbol:", symbol);
        console.log("Max Supply:", maxSupply);
        console.log("Mint Price:", mintPrice);

        vm.startBroadcast();

        NFTCollection nft = new NFTCollection(
            name,
            symbol,
            maxSupply,
            mintPrice,
            unrevealedURI
        );

        vm.stopBroadcast();

        console.log("NFT Collection deployed to:", address(nft));
        console.log("Owner:", nft.owner());

        return nft;
    }
}
