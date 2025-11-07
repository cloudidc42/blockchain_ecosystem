"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ==================== Block Models ====================

class BlockBase(BaseModel):
    """Base block information"""
    number: int
    hash: str
    parent_hash: str = Field(..., alias="parentHash")
    timestamp: int
    miner: str
    difficulty: int
    total_difficulty: int = Field(..., alias="totalDifficulty")
    size: int
    gas_limit: int = Field(..., alias="gasLimit")
    gas_used: int = Field(..., alias="gasUsed")
    transaction_count: int = Field(..., alias="transactionCount")

    class Config:
        populate_by_name = True


class BlockDetail(BlockBase):
    """Detailed block information"""
    nonce: str
    extra_data: str = Field(..., alias="extraData")
    transactions: List[str]  # Transaction hashes
    base_fee_per_gas: Optional[int] = Field(None, alias="baseFeePerGas")

    class Config:
        populate_by_name = True


class BlockList(BaseModel):
    """Paginated block list response"""
    blocks: List[BlockBase]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_prev: bool


# ==================== Transaction Models ====================

class TransactionBase(BaseModel):
    """Base transaction information"""
    hash: str
    block_number: int = Field(..., alias="blockNumber")
    from_address: str = Field(..., alias="from")
    to_address: Optional[str] = Field(None, alias="to")
    value: str  # Wei amount as string
    gas: int
    gas_price: int = Field(..., alias="gasPrice")
    nonce: int
    transaction_index: int = Field(..., alias="transactionIndex")

    class Config:
        populate_by_name = True


class TransactionDetail(TransactionBase):
    """Detailed transaction information"""
    input: str
    block_hash: str = Field(..., alias="blockHash")
    v: Optional[int] = None
    r: Optional[str] = None
    s: Optional[str] = None

    class Config:
        populate_by_name = True


class TransactionReceipt(BaseModel):
    """Transaction receipt"""
    transaction_hash: str = Field(..., alias="transactionHash")
    block_number: int = Field(..., alias="blockNumber")
    block_hash: str = Field(..., alias="blockHash")
    from_address: str = Field(..., alias="from")
    to_address: Optional[str] = Field(None, alias="to")
    gas_used: int = Field(..., alias="gasUsed")
    cumulative_gas_used: int = Field(..., alias="cumulativeGasUsed")
    effective_gas_price: Optional[int] = Field(None, alias="effectiveGasPrice")
    status: int  # 1 = success, 0 = failed
    logs: List[dict]
    contract_address: Optional[str] = Field(None, alias="contractAddress")

    class Config:
        populate_by_name = True


# ==================== Address Models ====================

class AddressInfo(BaseModel):
    """Address information"""
    address: str
    balance: str  # Wei as string
    balance_eth: float  # ETH as float
    transaction_count: int
    is_contract: bool


class AddressTransaction(BaseModel):
    """Transaction involving an address"""
    hash: str
    block_number: int
    timestamp: int
    from_address: str
    to_address: Optional[str]
    value: str
    gas_used: int
    status: int


# ==================== Statistics Models ====================

class BlockchainStats(BaseModel):
    """Blockchain statistics"""
    latest_block: int
    total_transactions: int
    avg_block_time: float  # seconds
    avg_gas_price: int  # wei
    network_hashrate: Optional[str] = None
    difficulty: int
    pending_transactions: int


class GasStats(BaseModel):
    """Gas price statistics"""
    slow: int  # Gwei
    standard: int  # Gwei
    fast: int  # Gwei
    instant: int  # Gwei
    base_fee: Optional[int] = None  # Wei


# ==================== Common Models ====================

class HealthCheck(BaseModel):
    """API health check response"""
    status: str
    version: str
    connected: bool
    latest_block: Optional[int] = None
    chain_id: Optional[int] = None


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
    status_code: int


class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
