# api/v1/user.py
"""User API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserOut, UserUpdate
from crud.user import get_user_by_username, create_user, update_user, delete_user
from api.deps import get_current_active_user
from core.database import get_db  # Import get_db directly
from models.db_models import User

router = APIRouter(prefix="/user", tags=["users"])

@router.get("/{username}", response_model=UserOut)
async def read_user(username: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Retrieve a user by username."""
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail={"errCode": 404, "errMsg": "User not found"})
    return user

@router.post("/", response_model=UserOut)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Create a new user (non-superuser)."""
    return create_user(db, user)

@router.put("/{username}", response_model=UserOut)
async def update_existing_user(username: str, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Update a user by username."""
    return update_user(db, username, user)

@router.delete("/{username}")
async def remove_user(username: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Delete a user by username."""
    delete_user(db, username)
    return {"message": "User deleted"}