# schemas/inventory.py
"""Pydantic schemas for Inventory model."""

from pydantic import BaseModel, Field, UUID4
from typing import Optional
from datetime import datetime

class InventoryBase(BaseModel):
    product_id: UUID4
    qty: float = Field(..., ge=0)
    type: str = Field(..., min_length=1)
    source: Optional[str] = None
    destination: Optional[str] = None
    created_time: datetime
    created_by: str = Field(..., min_length=1)
    remark: Optional[str] = None

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    product_id: Optional[UUID4] = None
    qty: Optional[float] = Field(None, ge=0)
    type: Optional[str] = Field(None, min_length=1)
    source: Optional[str] = None
    destination: Optional[str] = None
    created_time: Optional[datetime] = None
    created_by: Optional[str] = Field(None, min_length=1)
    remark: Optional[str] = None

class InventoryOut(InventoryBase):
    id: UUID4

    class Config:
        from_attributes = True
        json_encoders = {
            UUID4: lambda v: str(v)
        }