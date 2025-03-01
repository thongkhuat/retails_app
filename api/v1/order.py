# api/v1/order.py
"""Order API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.order import OrderCreate, OrderOut, OrderUpdate
from crud.order import create_order, update_order, delete_order
from api.deps import get_db_session, get_current_active_user
from models.db_models import User

router = APIRouter(prefix="/order", tags=["orders"])

@router.post("/", response_model=OrderOut)
async def create_new_order(order: OrderCreate, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_active_user)):
    """Create a new order with details."""
    return create_order(db, order)

@router.put("/{order_id}", response_model=OrderOut)
async def update_existing_order(order_id: str, order: OrderUpdate, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_active_user)):
    """Update an order with details by ID."""
    return update_order(db, order_id, order)

@router.delete("/{order_id}")
async def remove_order(order_id: str, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_active_user)):
    """Delete an order and its details by ID."""
    delete_order(db, order_id)
    return {"message": "Order deleted"}