"""
Address API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from ..models.schemas import AddressInfo
from ..services import blockchain_service

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.get("/{address}", response_model=AddressInfo, summary="Get address information")
async def get_address_info(address: str):
    """
    Get address information including balance and transaction count

    - **address**: Ethereum address (0x...)

    Returns:
    - Balance in Wei and ETH
    - Transaction count (nonce)
    - Whether address is a contract
    """
    try:
        # Validate address format
        if not address.startswith('0x') or len(address) != 42:
            raise HTTPException(
                status_code=400,
                detail="Invalid address format. Must be 42 characters starting with 0x"
            )

        # Get address data
        balance_wei = blockchain_service.get_balance(address)
        balance_eth = blockchain_service.wei_to_eth(balance_wei)
        tx_count = blockchain_service.get_transaction_count(address)
        is_contract = blockchain_service.is_contract(address)

        return AddressInfo(
            address=address,
            balance=str(balance_wei),
            balance_eth=balance_eth,
            transaction_count=tx_count,
            is_contract=is_contract
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{address}/balance", response_model=dict, summary="Get address balance")
async def get_address_balance(
    address: str,
    unit: str = Query("wei", regex="^(wei|gwei|ether)$", description="Unit: wei, gwei, or ether")
):
    """
    Get address balance in specified unit

    - **address**: Ethereum address
    - **unit**: wei, gwei, or ether (default: wei)
    """
    try:
        balance_wei = blockchain_service.get_balance(address)

        if unit == "ether":
            balance = blockchain_service.wei_to_eth(balance_wei)
        elif unit == "gwei":
            balance = balance_wei / 1e9
        else:  # wei
            balance = balance_wei

        return {
            "address": address,
            "balance": balance,
            "unit": unit
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{address}/code", response_model=dict, summary="Get contract code")
async def get_contract_code(address: str):
    """
    Get contract bytecode at address

    - **address**: Contract address

    Returns empty (0x) if not a contract
    """
    try:
        code = blockchain_service.get_code(address)
        is_contract = code != "0x" and code != "0x0"

        return {
            "address": address,
            "code": code,
            "is_contract": is_contract,
            "code_size": len(code) // 2 - 1  # Hex length to bytes
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
