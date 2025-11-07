"""
Transaction API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from ..models.schemas import TransactionDetail, TransactionReceipt
from ..services import blockchain_service

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/{tx_hash}", response_model=TransactionDetail, summary="Get transaction by hash")
async def get_transaction(tx_hash: str):
    """
    Get detailed transaction information

    - **tx_hash**: Transaction hash (0x...)
    """
    try:
        # Ensure hash starts with 0x
        if not tx_hash.startswith('0x'):
            tx_hash = '0x' + tx_hash

        tx = blockchain_service.get_transaction(tx_hash)

        if not tx:
            raise HTTPException(
                status_code=404,
                detail=f"Transaction {tx_hash} not found"
            )

        return TransactionDetail(**tx)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{tx_hash}/receipt", response_model=TransactionReceipt, summary="Get transaction receipt")
async def get_transaction_receipt(tx_hash: str):
    """
    Get transaction receipt

    - **tx_hash**: Transaction hash (0x...)

    Returns receipt with status, gas used, logs, etc.
    """
    try:
        # Ensure hash starts with 0x
        if not tx_hash.startswith('0x'):
            tx_hash = '0x' + tx_hash

        receipt = blockchain_service.get_transaction_receipt(tx_hash)

        if not receipt:
            raise HTTPException(
                status_code=404,
                detail=f"Transaction receipt for {tx_hash} not found"
            )

        return TransactionReceipt(**receipt)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pending/count", response_model=int, summary="Get pending transaction count")
async def get_pending_count():
    """Get number of pending transactions in mempool"""
    try:
        return blockchain_service.get_pending_transaction_count()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
