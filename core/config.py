# core/config.py
"""Application configuration settings."""

import os
import secrets

class Settings:
    """Configuration class for the app."""
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))  # Random key for local dev
    ALGORITHM: str = "HS256"  # JWT encryption algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Token expiration time
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///retail.db")  # Default to local SQLite

settings = Settings()