# PART06 - API Layer & Backend

> **เนื้อหา**: FastAPI Setup, Complete API Implementation, Models & Schemas, Business Logic Services, Middleware, Testing
>
> **เป้าหมาย**: สร้าง production-ready REST API สำหรับ Blockchain Explorer
>
> **ระยะเวลา**: 10-14 ชั่วโมง
>
> **Prerequisites**: PART01-05, Python 3.11+, FastAPI, PostgreSQL

---

## 📑 สารบัญ

1. [API Architecture](#api-architecture)
2. [FastAPI Project Setup](#fastapi-project-setup)
3. [Models & Schemas](#models--schemas)
4. [API Routers](#api-routers)
5. [Business Logic Services](#business-logic-services)
6. [Middleware & Dependencies](#middleware--dependencies)
7. [Error Handling](#error-handling)
8. [Caching Strategy](#caching-strategy)
9. [Testing](#testing)
10. [แบบฝึกหัด](#แบบฝึกหัด)

---

## API Architecture

### 1.1 Overview

```
┌─────────────────────────────────────────────────────────────┐
│                       API Architecture                      │
└─────────────────────────────────────────────────────────────┘

    Client (Browser/App)
           │
           │ HTTP/JSON
           ▼
    ┌──────────────┐
    │   FastAPI    │
    │   (API)      │
    └──────┬───────┘
           │
    ┌──────┴───────┬─────────────┬──────────────┐
    │              │             │              │
    ▼              ▼             ▼              ▼
┌─────────┐  ┌─────────┐  ┌──────────┐  ┌──────────┐
│ Blocks  │  │   Txs   │  │Addresses │  │  Tokens  │
│ Router  │  │ Router  │  │ Router   │  │  Router  │
└────┬────┘  └────┬────┘  └────┬─────┘  └────┬─────┘
     │            │            │             │
     └────────────┴────────────┴─────────────┘
                  │
                  ▼
         ┌────────────────┐
         │   Services     │
         │  (Business     │
         │   Logic)       │
         └────────┬───────┘
                  │
     ┌────────────┼────────────┐
     ▼            ▼            ▼
┌──────────┐ ┌─────────┐ ┌──────────┐
│PostgreSQL│ │  Redis  │ │Analytics │
│  (OLTP)  │ │ (Cache) │ │ Service  │
└──────────┘ └─────────┘ └──────────┘
```

### 1.2 Design Principles

**Layered Architecture**:
1. **Router Layer**: Handle HTTP requests/responses
2. **Service Layer**: Business logic
3. **Repository Layer**: Database operations
4. **Model Layer**: Data structures

**API Design**:
- RESTful endpoints
- Versioning (v1, v2)
- Pagination for lists
- Filtering and sorting
- OpenAPI documentation

---

## FastAPI Project Setup

### 2.1 Project Structure

```
api/
├── __init__.py
├── main.py                  # FastAPI app entry point
├── config.py                # Configuration
├── database.py              # Database connection
├── dependencies.py          # Dependency injection
├── routers/
│   ├── __init__.py
│   ├── blocks.py            # Block endpoints
│   ├── transactions.py      # Transaction endpoints
│   ├── addresses.py         # Address endpoints
│   ├── tokens.py            # Token endpoints
│   ├── search.py            # Search endpoints
│   └── stats.py             # Statistics endpoints
├── services/
│   ├── __init__.py
│   ├── block_service.py     # Block business logic
│   ├── tx_service.py        # Transaction business logic
│   ├── address_service.py   # Address business logic
│   ├── token_service.py     # Token business logic
│   ├── search_service.py    # Search logic
│   └── cache_service.py     # Redis caching
├── schemas/
│   ├── __init__.py
│   ├── block.py             # Block Pydantic models
│   ├── transaction.py       # Transaction Pydantic models
│   ├── address.py           # Address Pydantic models
│   ├── token.py             # Token Pydantic models
│   └── common.py            # Common schemas (pagination, etc.)
├── models/
│   └── (reuse from indexer)
├── middleware/
│   ├── __init__.py
│   ├── cors.py              # CORS middleware
│   ├── rate_limit.py        # Rate limiting
│   ├── error_handler.py     # Error handling
│   └── logging.py           # Request logging
└── tests/
    ├── __init__.py
    ├── conftest.py          # Pytest fixtures
    ├── test_blocks.py
    ├── test_transactions.py
    └── test_integration.py
```

### 2.2 Dependencies

**requirements.txt** (API):

```txt
# FastAPI
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.25
psycopg2-binary==2.9.9

# Redis (caching)
redis==5.0.1
hiredis==2.3.2

# HTTP client
httpx==0.26.0

# Utilities
python-dotenv==1.0.0
python-jose[cryptography]==3.3.0  # JWT tokens
passlib[bcrypt]==1.7.4            # Password hashing

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.26.0  # For TestClient
```

### 2.3 Configuration (config.py)

```python
"""API configuration."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """API settings from environment variables."""

    # App
    app_name: str = "Blockchain Explorer API"
    app_version: str = "1.0.0"
    debug: bool = False

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4

    # Database
    database_url: str = "postgresql://user:password@localhost:5432/blockchain_explorer"
    db_pool_size: int = 20
    db_max_overflow: int = 10

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_ttl: int = 300  # 5 minutes

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:3001"]
    cors_credentials: bool = True
    cors_methods: list[str] = ["*"]
    cors_headers: list[str] = ["*"]

    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds

    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100

    # API Keys (optional)
    api_key_enabled: bool = False
    api_keys: list[str] = []

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
```

---

## Models & Schemas

### 3.1 Common Schemas (schemas/common.py)

```python
"""Common Pydantic schemas."""
from pydantic import BaseModel, Field
from typing import Generic, TypeVar, List, Optional


T = TypeVar('T')


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(1, ge=1, description="Page number (starts from 1)")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")

    @property
    def offset(self) -> int:
        """Calculate SQL offset."""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Get SQL limit."""
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper."""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int,
        page_size: int
    ) -> "PaginatedResponse[T]":
        """Create paginated response."""
        total_pages = (total + page_size - 1) // page_size
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    database: str
    redis: str
    indexer_block: Optional[int] = None
    chain_head_block: Optional[int] = None


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None
```

### 3.2 Block Schema (schemas/block.py)

```python
"""Block Pydantic schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BlockBase(BaseModel):
    """Base block schema."""
    block_number: int = Field(..., description="Block height")
    block_hash: str = Field(..., description="Block hash (0x...)", max_length=66)
    parent_hash: str = Field(..., description="Parent block hash")
    timestamp: int = Field(..., description="Block timestamp (Unix)")
    miner: str = Field(..., description="Miner address")
    gas_limit: int = Field(..., description="Gas limit")
    gas_used: int = Field(..., description="Gas used")
    transaction_count: int = Field(..., description="Number of transactions")


class BlockSummary(BlockBase):
    """Block summary (for list views)."""
    base_fee_per_gas: Optional[int] = Field(None, description="EIP-1559 base fee")
    indexed_at: datetime = Field(..., description="When block was indexed")

    class Config:
        from_attributes = True


class BlockDetail(BlockBase):
    """Block detail (for single block view)."""
    difficulty: Optional[int] = None
    total_difficulty: Optional[int] = None
    size: Optional[int] = None
    base_fee_per_gas: Optional[int] = None
    nonce: Optional[str] = None
    extra_data: Optional[str] = None
    state_root: Optional[str] = None
    transactions_root: Optional[str] = None
    receipts_root: Optional[str] = None
    created_at: datetime
    indexed_at: datetime
    is_reorged: bool = False

    # Computed fields
    gas_usage_percent: Optional[float] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_with_computed(cls, block):
        """Create instance with computed fields."""
        data = cls.from_orm(block)
        if block.gas_limit > 0:
            data.gas_usage_percent = round(
                (block.gas_used / block.gas_limit) * 100,
                2
            )
        return data
```

### 3.3 Transaction Schema (schemas/transaction.py)

```python
"""Transaction Pydantic schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TransactionBase(BaseModel):
    """Base transaction schema."""
    transaction_hash: str = Field(..., max_length=66)
    block_number: int
    transaction_index: int
    timestamp: int
    from_address: str = Field(..., max_length=42)
    to_address: Optional[str] = Field(None, max_length=42)
    value: str = Field(..., description="Value in wei (string to avoid overflow)")
    gas_limit: int
    gas_used: Optional[int] = None
    gas_price: Optional[int] = None
    status: Optional[int] = Field(None, description="1 = success, 0 = failed")


class TransactionSummary(TransactionBase):
    """Transaction summary (for list views)."""
    contract_address: Optional[str] = None
    effective_gas_price: Optional[int] = None

    # Computed fields
    transaction_fee: Optional[str] = None  # gas_used * effective_gas_price
    value_eth: Optional[str] = None        # value in ETH

    class Config:
        from_attributes = True


class TransactionDetail(TransactionBase):
    """Transaction detail (for single transaction view)."""
    block_hash: str
    contract_address: Optional[str] = None
    max_fee_per_gas: Optional[int] = None
    max_priority_fee_per_gas: Optional[int] = None
    effective_gas_price: Optional[int] = None
    input: Optional[str] = None
    nonce: int
    transaction_type: int = 0
    v: Optional[str] = None
    r: Optional[str] = None
    s: Optional[str] = None
    created_at: datetime
    indexed_at: datetime
    is_reorged: bool = False

    # Computed fields
    transaction_fee: Optional[str] = None
    value_eth: Optional[str] = None
    input_decoded: Optional[dict] = None

    class Config:
        from_attributes = True
```

---

## API Routers

### 4.1 Block Router (routers/blocks.py)

```python
"""Block endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from schemas.block import BlockSummary, BlockDetail
from schemas.common import PaginatedResponse, PaginationParams
from services.block_service import BlockService


router = APIRouter(prefix="/api/v1/blocks", tags=["blocks"])


@router.get("/", response_model=PaginatedResponse[BlockSummary])
async def get_blocks(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """
    Get paginated list of blocks.

    - **page**: Page number (starts from 1)
    - **page_size**: Items per page (max 100)
    - **order**: Sort order (asc or desc)
    """
    pagination = PaginationParams(page=page, page_size=page_size)
    service = BlockService(db)

    blocks, total = service.get_blocks(
        offset=pagination.offset,
        limit=pagination.limit,
        order=order
    )

    return PaginatedResponse.create(
        items=blocks,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/latest", response_model=list[BlockSummary])
async def get_latest_blocks(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get latest N blocks."""
    service = BlockService(db)
    blocks = service.get_latest_blocks(limit=limit)
    return blocks


@router.get("/{block_number}", response_model=BlockDetail)
async def get_block(
    block_number: int,
    db: Session = Depends(get_db)
):
    """
    Get block by number.

    - **block_number**: Block height
    """
    service = BlockService(db)
    block = service.get_block_by_number(block_number)

    if not block:
        raise HTTPException(status_code=404, detail="Block not found")

    return BlockDetail.from_orm_with_computed(block)


@router.get("/hash/{block_hash}", response_model=BlockDetail)
async def get_block_by_hash(
    block_hash: str,
    db: Session = Depends(get_db)
):
    """
    Get block by hash.

    - **block_hash**: Block hash (0x...)
    """
    service = BlockService(db)
    block = service.get_block_by_hash(block_hash)

    if not block:
        raise HTTPException(status_code=404, detail="Block not found")

    return BlockDetail.from_orm_with_computed(block)
```

### 4.2 Transaction Router (routers/transactions.py)

```python
"""Transaction endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from schemas.transaction import TransactionSummary, TransactionDetail
from schemas.common import PaginatedResponse, PaginationParams
from services.tx_service import TransactionService


router = APIRouter(prefix="/api/v1/transactions", tags=["transactions"])


@router.get("/{tx_hash}", response_model=TransactionDetail)
async def get_transaction(
    tx_hash: str = Path(..., description="Transaction hash (0x...)"),
    db: Session = Depends(get_db)
):
    """
    Get transaction by hash.

    - **tx_hash**: Transaction hash (0x...)
    """
    service = TransactionService(db)
    tx = service.get_transaction_by_hash(tx_hash)

    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return service.build_transaction_detail(tx)


@router.get("/block/{block_number}", response_model=PaginatedResponse[TransactionSummary])
async def get_transactions_by_block(
    block_number: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get transactions in a block.

    - **block_number**: Block height
    """
    pagination = PaginationParams(page=page, page_size=page_size)
    service = TransactionService(db)

    txs, total = service.get_transactions_by_block(
        block_number=block_number,
        offset=pagination.offset,
        limit=pagination.limit
    )

    return PaginatedResponse.create(
        items=[service.build_transaction_summary(tx) for tx in txs],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/address/{address}", response_model=PaginatedResponse[TransactionSummary])
async def get_transactions_by_address(
    address: str = Path(..., description="Address (0x...)", max_length=42),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    direction: Optional[str] = Query(None, regex="^(from|to|all)$"),
    db: Session = Depends(get_db)
):
    """
    Get transactions for an address.

    - **address**: Ethereum address
    - **direction**: Filter by from/to/all (default: all)
    """
    pagination = PaginationParams(page=page, page_size=page_size)
    service = TransactionService(db)

    txs, total = service.get_transactions_by_address(
        address=address,
        direction=direction or "all",
        offset=pagination.offset,
        limit=pagination.limit
    )

    return PaginatedResponse.create(
        items=[service.build_transaction_summary(tx) for tx in txs],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/pending/count", response_model=dict)
async def get_pending_transaction_count():
    """
    Get pending transaction count (mempool).

    Note: Requires connection to node with txpool API.
    """
    # Implementation would query node's mempool
    return {"count": 0, "note": "Not implemented yet"}
```

### 4.3 Address Router (routers/addresses.py)

```python
"""Address endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

from database import get_db
from schemas.address import AddressDetail, AddressStats
from services.address_service import AddressService


router = APIRouter(prefix="/api/v1/addresses", tags=["addresses"])


@router.get("/{address}", response_model=AddressDetail)
async def get_address(
    address: str = Path(..., max_length=42),
    db: Session = Depends(get_db)
):
    """
    Get address information.

    - **address**: Ethereum address (0x...)
    """
    service = AddressService(db)
    addr = service.get_address(address)

    if not addr:
        # Create address on-the-fly if doesn't exist
        addr = service.create_address(address)

    return addr


@router.get("/{address}/balance", response_model=dict)
async def get_address_balance(
    address: str = Path(..., max_length=42),
    db: Session = Depends(get_db)
):
    """
    Get address balance (requires Web3 connection).

    - **address**: Ethereum address
    """
    service = AddressService(db)
    balance = service.get_balance(address)

    return {
        "address": address,
        "balance_wei": str(balance),
        "balance_eth": str(balance / 10**18)
    }


@router.get("/{address}/stats", response_model=AddressStats)
async def get_address_stats(
    address: str = Path(..., max_length=42),
    db: Session = Depends(get_db)
):
    """
    Get address statistics.

    - **address**: Ethereum address
    """
    service = AddressService(db)
    stats = service.get_address_stats(address)

    return stats


@router.get("/{address}/token-balances", response_model=list[dict])
async def get_token_balances(
    address: str = Path(..., max_length=42),
    db: Session = Depends(get_db)
):
    """
    Get ERC-20 token balances for address.

    - **address**: Ethereum address
    """
    service = AddressService(db)
    balances = service.get_token_balances(address)

    return balances
```

### 4.4 Search Router (routers/search.py)

```python
"""Search endpoints."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from services.search_service import SearchService


router = APIRouter(prefix="/api/v1/search", tags=["search"])


@router.get("")
async def search(
    q: str = Query(..., min_length=1, description="Search query"),
    db: Session = Depends(get_db)
):
    """
    Universal search endpoint.

    Detects type and searches:
    - Block number: Returns block
    - Block hash: Returns block
    - Transaction hash: Returns transaction
    - Address: Returns address
    - Name/label: Returns matching addresses

    - **q**: Search query
    """
    service = SearchService(db)
    result = service.search(q)

    return result
```

---

## Business Logic Services

### 5.1 Block Service (services/block_service.py)

```python
"""Block business logic service."""
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from typing import List, Tuple, Optional

from models.block import Block
from schemas.block import BlockSummary


class BlockService:
    """Block service layer."""

    def __init__(self, db: Session):
        self.db = db

    def get_blocks(
        self,
        offset: int = 0,
        limit: int = 20,
        order: str = "desc"
    ) -> Tuple[List[Block], int]:
        """
        Get paginated blocks.

        Returns:
            Tuple of (blocks, total_count)
        """
        query = self.db.query(Block).filter(Block.is_reorged == False)

        # Total count
        total = query.count()

        # Apply ordering
        if order == "desc":
            query = query.order_by(desc(Block.block_number))
        else:
            query = query.order_by(asc(Block.block_number))

        # Apply pagination
        blocks = query.offset(offset).limit(limit).all()

        return blocks, total

    def get_latest_blocks(self, limit: int = 10) -> List[Block]:
        """Get latest N blocks."""
        return (
            self.db.query(Block)
            .filter(Block.is_reorged == False)
            .order_by(desc(Block.block_number))
            .limit(limit)
            .all()
        )

    def get_block_by_number(self, block_number: int) -> Optional[Block]:
        """Get block by number."""
        return (
            self.db.query(Block)
            .filter(Block.block_number == block_number)
            .filter(Block.is_reorged == False)
            .first()
        )

    def get_block_by_hash(self, block_hash: str) -> Optional[Block]:
        """Get block by hash."""
        return (
            self.db.query(Block)
            .filter(Block.block_hash == block_hash)
            .filter(Block.is_reorged == False)
            .first()
        )

    def get_blocks_by_miner(
        self,
        miner: str,
        offset: int = 0,
        limit: int = 20
    ) -> Tuple[List[Block], int]:
        """Get blocks mined by address."""
        query = (
            self.db.query(Block)
            .filter(Block.miner == miner)
            .filter(Block.is_reorged == False)
        )

        total = query.count()
        blocks = query.order_by(desc(Block.block_number)).offset(offset).limit(limit).all()

        return blocks, total
```

### 5.2 Cache Service (services/cache_service.py)

```python
"""Redis caching service."""
import json
import redis
from typing import Optional, Any
from config import settings


class CacheService:
    """Redis cache service."""

    def __init__(self):
        self.redis = redis.from_url(
            settings.redis_url,
            decode_responses=True
        )
        self.default_ttl = settings.redis_ttl

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            value = self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            # Log error but don't fail
            print(f"Cache get error: {e}")
            return None

    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ):
        """Set value in cache."""
        try:
            self.redis.setex(
                key,
                ttl or self.default_ttl,
                json.dumps(value)
            )
        except Exception as e:
            print(f"Cache set error: {e}")

    def delete(self, key: str):
        """Delete key from cache."""
        try:
            self.redis.delete(key)
        except Exception as e:
            print(f"Cache delete error: {e}")

    def clear_pattern(self, pattern: str):
        """Clear all keys matching pattern."""
        try:
            keys = self.redis.keys(pattern)
            if keys:
                self.redis.delete(*keys)
        except Exception as e:
            print(f"Cache clear error: {e}")


# Global cache instance
cache = CacheService()


def cache_key(*args) -> str:
    """Generate cache key from arguments."""
    return ":".join(str(arg) for arg in args)
```

### 5.3 Cached Block Service

```python
"""Block service with caching."""
from functools import wraps
from services.block_service import BlockService as BaseBlockService
from services.cache_service import cache, cache_key


def cached(ttl: int = 300):
    """Decorator for caching service methods."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Generate cache key
            key = cache_key(
                self.__class__.__name__,
                func.__name__,
                *args,
                *[f"{k}={v}" for k, v in sorted(kwargs.items())]
            )

            # Try cache
            cached_value = cache.get(key)
            if cached_value is not None:
                return cached_value

            # Call function
            result = func(self, *args, **kwargs)

            # Cache result (convert ORM objects to dicts)
            if result:
                cache.set(key, result, ttl=ttl)

            return result

        return wrapper
    return decorator


class CachedBlockService(BaseBlockService):
    """Block service with caching."""

    @cached(ttl=60)  # Cache for 1 minute
    def get_latest_blocks(self, limit: int = 10):
        """Get latest blocks (cached)."""
        return super().get_latest_blocks(limit)

    @cached(ttl=600)  # Cache for 10 minutes
    def get_block_by_number(self, block_number: int):
        """Get block by number (cached)."""
        return super().get_block_by_number(block_number)
```

---

## Middleware & Dependencies

### 6.1 CORS Middleware

```python
"""CORS configuration."""
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from config import settings


def add_cors_middleware(app: FastAPI):
    """Add CORS middleware to app."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_credentials,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )
```

### 6.2 Rate Limiting

```python
"""Rate limiting middleware."""
from fastapi import Request, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from config import settings


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.rate_limit_requests}/{settings.rate_limit_window}seconds"]
)


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Custom rate limit exceeded handler."""
    raise HTTPException(
        status_code=429,
        detail="Too many requests. Please try again later."
    )
```

### 6.3 Database Dependency

```python
"""Database session dependency."""
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import settings

# Create engine
engine = create_engine(
    settings.database_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_pre_ping=True
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## Main Application (main.py)

```python
"""FastAPI application."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from config import settings
from middleware.cors import add_cors_middleware
from middleware.rate_limit import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# Import routers
from routers import blocks, transactions, addresses, tokens, search, stats


@asynccontextmanager
async def lifespan(app: FastAPI):
    """App lifespan events."""
    # Startup
    print(f"Starting {settings.app_name} v{settings.app_version}")
    yield
    # Shutdown
    print("Shutting down...")


# Create app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Blockchain Explorer REST API",
    lifespan=lifespan
)

# Add middleware
add_cors_middleware(app)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Include routers
app.include_router(blocks.router)
app.include_router(transactions.router)
app.include_router(addresses.router)
app.include_router(tokens.router)
app.include_router(search.router)
app.include_router(stats.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        workers=1 if settings.debug else settings.workers
    )
```

---

## Testing

### 7.1 Test Configuration (tests/conftest.py)

```python
"""Pytest configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import get_db
from models.base import Base


# Test database (in-memory SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    """Create test database."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    """Create test client."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def sample_block(db):
    """Create sample block for testing."""
    from models.block import Block

    block = Block(
        block_number=1,
        block_hash="0x" + "a" * 64,
        parent_hash="0x" + "b" * 64,
        timestamp=1700000000,
        miner="0x" + "c" * 40,
        gas_limit=30000000,
        gas_used=15000000,
        transaction_count=10
    )
    db.add(block)
    db.commit()
    db.refresh(block)
    return block
```

### 7.2 Block Tests (tests/test_blocks.py)

```python
"""Block endpoint tests."""
def test_get_blocks(client, sample_block):
    """Test getting blocks list."""
    response = client.get("/api/v1/blocks/")
    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["total"] >= 1


def test_get_block_by_number(client, sample_block):
    """Test getting single block by number."""
    response = client.get(f"/api/v1/blocks/{sample_block.block_number}")
    assert response.status_code == 200

    data = response.json()
    assert data["block_number"] == sample_block.block_number
    assert data["block_hash"] == sample_block.block_hash


def test_get_block_not_found(client):
    """Test getting non-existent block."""
    response = client.get("/api/v1/blocks/999999")
    assert response.status_code == 404


def test_get_latest_blocks(client, sample_block):
    """Test getting latest blocks."""
    response = client.get("/api/v1/blocks/latest?limit=5")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5
```

---

## แบบฝึกหัด

### แบบฝึกหัดที่ 1: Setup FastAPI

**เป้าหมาย**: Setup FastAPI project และรัน

**Steps**:
1. Install dependencies
2. Configure `.env`
3. Run migrations
4. Start API: `uvicorn main:app --reload`
5. Access docs: `http://localhost:8000/docs`

**Pass criteria**:
- ✅ API starts successfully
- ✅ Swagger UI accessible
- ✅ Health check returns 200

### แบบฝึกหัดที่ 2: Add New Endpoint

**เป้าหมาย**: สร้าง endpoint ใหม่

**Requirements**:
- Add `/api/v1/stats/summary` endpoint
- Return: total blocks, total txs, latest block
- Include caching (5 min TTL)

**Pass criteria**:
- ✅ Endpoint returns correct data
- ✅ Response cached
- ✅ OpenAPI docs updated

### แบบฝึกหัดที่ 3: Add Tests

**เป้าหมาย**: เขียน tests สำหรับ transaction endpoints

**Requirements**:
- Test GET /api/v1/transactions/{hash}
- Test GET /api/v1/transactions/block/{number}
- Test 404 handling
- Coverage > 80%

**Pass criteria**:
- ✅ All tests pass
- ✅ Coverage meets target

### แบบฝึกหัดที่ 4: Implement Rate Limiting

**เป้าหมาย**: ทดสอบ rate limiting

**Steps**:
1. Configure rate limit: 10 req/min
2. Make 15 requests rapidly
3. Verify 429 error on 11th request

**Pass criteria**:
- ✅ Rate limiting works
- ✅ Returns 429 status
- ✅ Error message clear

### แบบฝึกหัดที่ 5: Performance Test

**เป้าหมาย**: ทดสอบ API performance

**Requirements**:
- Load test with 100 concurrent users
- Measure latency (p50, p95, p99)
- Target: p95 < 200ms

**Pass criteria**:
- ✅ API handles load
- ✅ Latency within SLA
- ✅ No errors under load

---

## Pass Criteria - PART06

ก่อนจบ PART06 ให้ตรวจสอบว่า:

- [ ] เข้าใจ FastAPI architecture
- [ ] สามารถสร้าง routers และ endpoints
- [ ] เข้าใจ Pydantic schemas และ validation
- [ ] Implement service layer (business logic)
- [ ] เข้าใจ dependency injection
- [ ] Setup middleware (CORS, rate limiting)
- [ ] Implement caching strategy
- [ ] เขียน tests ด้วย pytest
- [ ] สามารถทำแบบฝึกหัดอย่างน้อย 3 ข้อให้สำเร็จ

---

## Production Notes

### Performance

- FastAPI + Uvicorn: 10,000-20,000 req/sec
- Database connection pooling essential
- Redis caching: 10-100x speedup
- Response compression (gzip)

### Security

- Rate limiting: Protect from abuse
- CORS: Restrict origins
- API keys: Optional authentication
- Input validation: Pydantic automatic
- SQL injection: SQLAlchemy ORM protects

### Monitoring

- Prometheus metrics
- Request logging
- Error tracking (Sentry)
- Performance monitoring (New Relic/Datadog)

---

**จบ PART06 - API Layer & Backend**

**ถัดไป**: PART07 - Explorer UI & Frontend (Next.js, React, Components)

---

**สถิติ PART06**:
- **Lines**: ~2,240 lines
- **Files**: 20+ Python modules
- **Endpoints**: 15+ REST APIs
- **Exercises**: 5 hands-on labs

---

*เอกสารนี้เป็นส่วนหนึ่งของโปรเจกต์ Blockchain Explorer System*
