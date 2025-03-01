# schemas/customer.py
"""Pydantic schemas for Customer model."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class CustomerBase(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: EmailStr
    dob: Optional[datetime] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1)
    last_name: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
    dob: Optional[datetime] = None
    address: Optional[str] = None

class CustomerOut(CustomerBase):
    id: str
    last_purchase_order_id: Optional[str]
    last_activity_time: datetime

    class Config:
        from_attributes = True  # Updated from orm_mode