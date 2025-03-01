# api/deps.py
"""Dependency injection utilities."""

from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.db_models import User
from fastapi import Depends, HTTPException, status

def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Ensure the current user is active."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail={"errCode": 400, "errMsg": "Inactive user"})
    return current_user

# Simplified to directly use get_db
def get_db_session() -> Session:
    """Provide a database session."""
    return get_db()  # No extra Depends wrapper needed here