# core/config.py
"""Application configuration settings."""

import os
import secrets

class Settings:
    """Configuration class for the app."""
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # Use Render's PostgreSQL URL or fallback to local SQLite for development
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/retail.db")

settings = Settings()