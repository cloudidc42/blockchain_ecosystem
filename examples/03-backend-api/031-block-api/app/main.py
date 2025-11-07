"""
Blockchain Explorer API
FastAPI application for interacting with Ethereum blockchain
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import time

from .core.config import settings
from .services import blockchain_service
from .routers import (
    blocks_router,
    transactions_router,
    addresses_router,
    stats_router,
)
from .models.schemas import HealthCheck, ErrorResponse


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📡 Connecting to blockchain node: {settings.RPC_URL}")

    try:
        is_connected = blockchain_service.is_connected()
        if is_connected:
            chain_id = blockchain_service.get_chain_id()
            latest_block = blockchain_service.get_latest_block_number()
            print(f"✅ Connected! Chain ID: {chain_id}, Latest Block: {latest_block}")
        else:
            print("⚠️  Warning: Cannot connect to blockchain node")
    except Exception as e:
        print(f"❌ Error connecting to blockchain: {e}")

    yield

    # Shutdown
    print(f"👋 Shutting down {settings.APP_NAME}")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    🔗 Blockchain Explorer API

    A comprehensive RESTful API for exploring Ethereum blockchain data.

    ## Features

    * 📦 **Blocks** - Get block information by number or hash
    * 💸 **Transactions** - Query transaction details and receipts
    * 👤 **Addresses** - Check balances and contract code
    * 📊 **Statistics** - Network stats and gas prices

    ## Authentication

    No authentication required for public endpoints.

    ## Rate Limiting

    Currently no rate limiting applied.
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add X-Process-Time header to responses"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    return response


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "detail": exc.errors(),
            "status_code": 422
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred",
            "status_code": 500
        }
    )


# Root endpoint
@app.get("/", tags=["Root"], summary="API Root")
async def root():
    """
    API root endpoint

    Returns basic API information and available endpoints
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "blocks": "/api/blocks",
            "transactions": "/api/transactions",
            "addresses": "/api/addresses",
            "stats": "/api/stats",
            "health": "/health"
        }
    }


# Health check endpoint
@app.get("/health", response_model=HealthCheck, tags=["Health"], summary="Health Check")
async def health_check():
    """
    Health check endpoint

    Returns API status and blockchain connection info
    """
    try:
        is_connected = blockchain_service.is_connected()
        latest_block = None
        chain_id = None

        if is_connected:
            latest_block = blockchain_service.get_latest_block_number()
            chain_id = blockchain_service.get_chain_id()

        return HealthCheck(
            status="healthy" if is_connected else "degraded",
            version=settings.APP_VERSION,
            connected=is_connected,
            latest_block=latest_block,
            chain_id=chain_id
        )
    except Exception as e:
        return HealthCheck(
            status="unhealthy",
            version=settings.APP_VERSION,
            connected=False,
            latest_block=None,
            chain_id=None
        )


# Include routers with /api prefix
app.include_router(blocks_router, prefix="/api")
app.include_router(transactions_router, prefix="/api")
app.include_router(addresses_router, prefix="/api")
app.include_router(stats_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
