"""
Application configuration management using Pydantic Settings.
This module handles all environment-based configuration.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.

    Usage:
        from app.core.config import settings

        # Access settings
        db_url = settings.DATABASE_URL
    """

    # Database Configuration
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    DATABASE_ECHO: bool = False  # Set to True to log all SQL queries

    # Application Settings
    APP_NAME: str = "Learning Async Python with FastAPI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True


    # API Configuration
    API_PREFIX: str = "/api"

    # External API Settings
    EXTERNAL_API_TIMEOUT: int = 10  # seconds

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # Ignore extra fields in .env
    )


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Dependency function to get settings instance.
    Useful for FastAPI dependency injection.

    Usage:
        @app.get("/config")
        async def get_config(settings: Settings = Depends(get_settings)):
            return {"database": settings.DATABASE_URL}
    """
    return settings