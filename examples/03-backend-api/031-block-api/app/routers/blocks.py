"""
Block API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..models.schemas import BlockDetail, BlockList, BlockBase
from ..services import blockchain_service
from ..core.config import settings

router = APIRouter(prefix="/blocks", tags=["Blocks"])


@router.get("/latest", response_model=int, summary="Get latest block number")
async def get_latest_block_number():
    """Get the latest block number"""
    try:
        return blockchain_service.get_latest_block_number()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=BlockList, summary="Get list of blocks")
async def get_blocks(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Blocks per page"),
    start_block: Optional[int] = Query(None, description="Starting block number (default: latest)")
):
    """
    Get paginated list of blocks

    - **page**: Page number (starts from 1)
    - **page_size**: Number of blocks per page (max 100)
    - **start_block**: Starting block number (default: latest)
    """
    try:
        if start_block is None:
            start_block = blockchain_service.get_latest_block_number()

        # Calculate offset
        offset = (page - 1) * page_size
        actual_start = start_block - offset

        # Get blocks
        blocks = blockchain_service.get_blocks(
            start_block=actual_start,
            limit=page_size,
            descending=True
        )

        # Convert to BlockBase models
        block_models = [BlockBase(**block) for block in blocks]

        # Calculate pagination info
        total_blocks = start_block + 1  # Approximate
        has_next = actual_start - page_size >= 0
        has_prev = page > 1

        return BlockList(
            blocks=block_models,
            total=total_blocks,
            page=page,
            page_size=page_size,
            has_next=has_next,
            has_prev=has_prev
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{block_number}", response_model=BlockDetail, summary="Get block by number")
async def get_block_by_number(
    block_number: int,
    full_transactions: bool = Query(False, description="Include full transaction details")
):
    """
    Get detailed block information

    - **block_number**: Block number
    - **full_transactions**: Return full transaction objects (default: false, returns hashes only)
    """
    try:
        block = blockchain_service.get_block(block_number, full_transactions=full_transactions)

        if not block:
            raise HTTPException(
                status_code=404,
                detail=f"Block {block_number} not found"
            )

        return BlockDetail(**block)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/hash/{block_hash}", response_model=BlockDetail, summary="Get block by hash")
async def get_block_by_hash(
    block_hash: str,
    full_transactions: bool = Query(False, description="Include full transaction details")
):
    """
    Get detailed block information by hash

    - **block_hash**: Block hash (0x...)
    - **full_transactions**: Return full transaction objects
    """
    try:
        block = blockchain_service.get_block(block_hash, full_transactions=full_transactions)

        if not block:
            raise HTTPException(
                status_code=404,
                detail=f"Block with hash {block_hash} not found"
            )

        return BlockDetail(**block)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
