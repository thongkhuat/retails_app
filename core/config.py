# core/config.py
"""Application configuration settings."""

import os
import secrets
from pathlib import Path

class Settings:
    """Configuration class for the app."""
    # Use pathlib for cross-platform path handling
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_PATH = BASE_DIR / "retail.db"

    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database URL from environment variable, with SQLite fallback
    DATABASE_URL: str = f"sqlite:///{DB_PATH.as_posix()}"

settings = Settings()