"""
Core configuration settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    APP_NAME: str = "Blockchain Explorer API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Web3 Settings
    RPC_URL: str = "http://localhost:8545"

    # CORS Settings
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Cache Settings (optional)
    CACHE_TTL: int = 60  # seconds

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
