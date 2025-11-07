"""
Statistics API endpoints
"""
from fastapi import APIRouter, HTTPException
from ..models.schemas import BlockchainStats, GasStats
from ..services import blockchain_service

router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get("/blockchain", response_model=BlockchainStats, summary="Get blockchain statistics")
async def get_blockchain_stats():
    """
    Get general blockchain statistics

    Returns:
    - Latest block number
    - Average block time
    - Average gas price
    - Network difficulty
    - Pending transactions
    """
    try:
        stats = blockchain_service.get_stats()

        # Estimate total transactions (approximation)
        # In production, this would come from a database
        total_tx = stats['latest_block'] * 150  # Approximate avg 150 tx/block

        return BlockchainStats(
            latest_block=stats['latest_block'],
            total_transactions=total_tx,
            avg_block_time=stats['avg_block_time'],
            avg_gas_price=stats['avg_gas_price'],
            difficulty=stats['difficulty'],
            pending_transactions=stats['pending_transactions']
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gas", response_model=GasStats, summary="Get gas price statistics")
async def get_gas_stats():
    """
    Get current gas price estimates

    Returns gas prices in Gwei for different speeds:
    - slow: Low priority
    - standard: Normal priority
    - fast: High priority
    - instant: Maximum priority
    """
    try:
        # Get current gas price
        gas_price_wei = blockchain_service.get_gas_price()
        gas_price_gwei = gas_price_wei / 1e9

        # Estimate different priority levels
        # In production, use EIP-1559 or gas price oracle
        return GasStats(
            slow=int(gas_price_gwei * 0.8),
            standard=int(gas_price_gwei),
            fast=int(gas_price_gwei * 1.2),
            instant=int(gas_price_gwei * 1.5),
            base_fee=gas_price_wei
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
