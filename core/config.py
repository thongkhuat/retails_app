# core/config.py
"""Application configuration settings."""

import os
import secrets
from pathlib import Path

class Settings:
    """Configuration class for the app."""
    # Use pathlib for cross-platform path handling
    BASE_DIR = Path(__file__).resolve().parent.parent
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # Database URL from environment variable, with SQLite fallback
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR}/retail.db"
    )

    def __post_init__(self):
        """Validate settings after initialization."""
        print(f"Using DATABASE_URL: {self.DATABASE_URL}")  # Debugging aid

settings = Settings()