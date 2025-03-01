# schemas/user.py
"""Pydantic schemas for User model."""

from pydantic import BaseModel, EmailStr, Field, UUID4
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=1)
    email: EmailStr
    role: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None

class UserOut(UserBase):
    id: UUID4  # Use UUID4 instead of str
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True
        json_encoders = {
            UUID4: lambda v: str(v)  # Convert UUID to string during serialization
        }