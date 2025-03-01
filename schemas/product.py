# schemas/product.py
"""Pydantic schemas for Product model."""

from pydantic import BaseModel, Field, UUID4
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1)
    type: str = Field(..., min_length=1)
    created_date: datetime
    retail_price: float = Field(..., gt=0)
    remark: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    type: Optional[str] = Field(None, min_length=1)
    created_date: Optional[datetime] = None
    retail_price: Optional[float] = Field(None, gt=0)
    remark: Optional[str] = None

class ProductOut(ProductBase):
    id: UUID4

    class Config:
        from_attributes = True
        json_encoders = {
            UUID4: lambda v: str(v)
        }