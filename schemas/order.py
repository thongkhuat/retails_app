# schemas/order.py
"""Pydantic schemas for Order and OrderDetail models."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class OrderDetailBase(BaseModel):
    product_id: str
    qty: float = Field(..., ge=0)
    discount: Optional[float] = Field(None, ge=0)
    retail_price: Optional[float] = Field(None, ge=0)
    real_price: Optional[float] = Field(None, ge=0)

class OrderDetailCreate(OrderDetailBase):
    pass

class OrderDetailUpdate(BaseModel):
    product_id: Optional[str] = None
    qty: Optional[float] = Field(None, ge=0)
    discount: Optional[float] = Field(None, ge=0)
    retail_price: Optional[float] = Field(None, ge=0)
    real_price: Optional[float] = Field(None, ge=0)

class OrderDetailOut(OrderDetailBase):
    id: str
    order_id: str

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    created_time: datetime
    customer_id: str
    is_delivered: bool
    note: Optional[str] = None
    delivered_time: Optional[datetime] = None
    total_retail_price: Optional[float] = None
    total_real_price: Optional[float] = None

class OrderCreate(OrderBase):
    details: List[OrderDetailCreate]

class OrderUpdate(BaseModel):
    created_time: Optional[datetime] = None
    customer_id: Optional[str] = None
    is_delivered: Optional[bool] = None
    note: Optional[str] = None
    delivered_time: Optional[datetime] = None
    total_retail_price: Optional[float] = None
    total_real_price: Optional[float] = None
    details: Optional[List[OrderDetailUpdate]] = None

class OrderOut(OrderBase):
    id: str
    details: List[OrderDetailOut]

    class Config:
        from_attributes = True  # Updated from orm_mode