"""
Configuration settings for AutoDevHub backend.

Uses pydantic-settings for environment variable management
and configuration validation.
"""

import os
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Based on ADR-003: Database Selection (SQLite)
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    api_host: str = Field(
        default="localhost",
        description="Host for the FastAPI application"
    )
    api_port: str = Field(
        default="8000",
        description="Port for the FastAPI application"
    )

    algorithm: str = Field(
        default="gpt-4",
        description="AI algorithm to use for story generation"
    )
    anthropic_api_key: str = Field(
        default=os.getenv("ANTHROPIC_API_KEY", ""),
        description="API key for Anthropic AI service"
    )
    allowed_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        description="Comma-separated list of allowed CORS origins"
    )
    phase1_status: str = Field(
        default="completed",
        description="Phase 1 status of the project"
    )
    phase1_completion_date: str = Field(
        default="2025-07-31",
        description="Expected completion date for Phase 1"
    )

    # Application Information
    app_name: str = Field(default="AutoDevHub", description="Application name")
    app_version: str = Field(
        default="1.0.0",
        description="Application version")
    app_description: str = Field(
        default="AI-Powered DevOps Tracker",
        description="Application description"
    )

    # Environment Configuration
    environment: str = Field(
        default="development",
        description="Application environment (development, testing, production)"\n    )

    # Database Configuration (ADR-003: SQLite)
    database_file: str = Field(
        default="autodevhub.db",
        description="SQLite database file path"
    )
    debug: bool = Field(
        default=False,
        description="Enable debug mode (shows SQL queries)"
    )
    create_sample_data: bool = Field(
        default=False,
        description="Create sample data on initialization"
    )

    # API Configuration
    api_prefix: str = Field(default="/api/v1", description="API URL prefix")
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins"
    )

    # Server Configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, ge=1, le=65535, description="Server port")
    reload: bool = Field(
        default=True,
        description="Enable auto-reload in development")

    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log message format"
    )

    # Performance Settings
    max_db_connections: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum concurrent database connections"
    )
    db_pool_size: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Database connection pool size"
    )

    # Health Check Configuration
    health_check_enabled: bool = Field(
        default=True,
        description="Enable health check endpoints"
    )

    # AI Integration (Future Enhancement)
    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API key for AI story generation"
    )
    ai_model: str = Field(
        default="gpt-4",
        description="AI model to use for story generation"
    )
    ai_max_tokens: int = Field(
        default=2000,
        ge=100,
        le=8000,
        description="Maximum tokens for AI generation"
    )

    # Security Settings (Future Enhancement)
    secret_key: Optional[str] = Field(
        default=None,
        description="Secret key for JWT token signing"
    )
    access_token_expire_minutes: int = Field(
        default=30,
        ge=1,
        le=60 * 24,  # Maximum 1 day
        description="Access token expiration time in minutes"
    )

    # Rate limiting settings
    rate_limit_requests: int = Field(
        default=100,
        ge=1,
        le=10000,
        description="Rate limit requests per window"
    )
    rate_limit_period: int = Field(
        default=60,
        ge=1,
        le=3600,
        description="Rate limit window in seconds"
    )

    # Database settings
    database_echo: bool = Field(
        default=False,
        description="Echo SQL queries (for development)"
    )

    @property
    def database_url(self) -> str:
        """
        Get the complete database URL for SQLAlchemy.

        Returns:
            SQLite database URL with aiosqlite driver
        """
        return "sqlite:///./autodevhub.db"

    @property
    def is_development(self) -> bool:
        """
        Check if running in development mode.

        Returns:
            True if in development mode
        """
        return self.debug or self.reload

    @property
    def database_file_path(self) -> Path:
        """
        Get the database file as a Path object.

        Returns:
            Path object for the database file
        """
        return Path(self.database_file)

    def get_database_info(self) -> dict:
        """
        Get information about the database configuration.

        Returns:
            Dictionary with database configuration info
        """
        db_path = self.database_file_path
        return {
            "database_file": str(db_path),
            "database_url": self.database_url,
            "exists": db_path.exists(),
            "size_bytes": db_path.stat().st_size if db_path.exists() else 0,
            "is_absolute": db_path.is_absolute(),
            "parent_directory": str(db_path.parent),
        }

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8"
    )


# Cached settings instance
@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


def get_testing_settings() -> Settings:
    """Get test-specific settings."""
    settings = Settings()
    settings.database_file = ":memory:"  # Use in-memory database for tests
    settings.database_echo = False
    settings.debug = True
    return settings


# Global settings instance
settings = Settings()
