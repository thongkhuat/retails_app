# crud/user.py
"""CRUD operations for User model."""

from sqlalchemy.orm import Session
from models.db_models import User
from schemas.user import UserCreate, UserUpdate
from core.auth_utils import get_password_hash  # Import from new module
from fastapi import HTTPException, status

def get_user_by_username(db: Session, username: str) -> User:
    """Retrieve a user by username."""
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: str) -> User:
    """Retrieve a user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user."""
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail={"errCode": 400, "errMsg": "Username already exists"})
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail={"errCode": 400, "errMsg": "Email already exists"})
    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
        role=user.role or "user",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, username: str, user_update: UserUpdate) -> User:
    """Update an existing user."""
    db_user = get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(status_code=404, detail={"errCode": 404, "errMsg": "User not found"})
    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, username: str) -> None:
    """Delete a user."""
    db_user = get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(status_code=404, detail={"errCode": 404, "errMsg": "User not found"})
    db.delete(db_user)
    db.commit()