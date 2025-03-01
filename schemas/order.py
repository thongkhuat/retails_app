# schemas/order.py
"""Pydantic schemas for Order and OrderDetail models."""

from pydantic import BaseModel, Field, UUID4
from typing import Optional, List
from datetime import datetime

class OrderDetailBase(BaseModel):
    product_id: UUID4
    qty: float = Field(..., ge=0)
    discount: Optional[float] = Field(None, ge=0)
    retail_price: Optional[float] = Field(None, ge=0)
    real_price: Optional[float] = Field(None, ge=0)

class OrderDetailCreate(OrderDetailBase):
    pass

class OrderDetailUpdate(BaseModel):
    product_id: Optional[UUID4] = None
    qty: Optional[float] = Field(None, ge=0)
    discount: Optional[float] = Field(None, ge=0)
    retail_price: Optional[float] = Field(None, ge=0)
    real_price: Optional[float] = Field(None, ge=0)

class OrderDetailOut(OrderDetailBase):
    id: UUID4
    order_id: UUID4

    class Config:
        from_attributes = True
        json_encoders = {
            UUID4: lambda v: str(v)
        }

class OrderBase(BaseModel):
    created_time: datetime
    customer_id: UUID4
    is_delivered: bool
    note: Optional[str] = None
    delivered_time: Optional[datetime] = None
    total_retail_price: Optional[float] = None
    total_real_price: Optional[float] = None

class OrderCreate(OrderBase):
    details: List[OrderDetailCreate]

class OrderUpdate(BaseModel):
    created_time: Optional[datetime] = None
    customer_id: Optional[UUID4] = None
    is_delivered: Optional[bool] = None
    note: Optional[str] = None
    delivered_time: Optional[datetime] = None
    total_retail_price: Optional[float] = None
    total_real_price: Optional[float] = None
    details: Optional[List[OrderDetailUpdate]] = None

class OrderOut(OrderBase):
    id: UUID4
    details: List[OrderDetailOut]

    class Config:
        from_attributes = True
        json_encoders = {
            UUID4: lambda v: str(v)
        }