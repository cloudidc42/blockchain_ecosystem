"""Routers package"""
from .blocks import router as blocks_router
from .transactions import router as transactions_router
from .addresses import router as addresses_router
from .stats import router as stats_router

__all__ = [
    "blocks_router",
    "transactions_router",
    "addresses_router",
    "stats_router",
]
