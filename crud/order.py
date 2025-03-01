# crud/order.py
"""CRUD operations for Order and OrderDetail models."""

from sqlalchemy.orm import Session
from models.db_models import Order, OrderDetail
from schemas.order import OrderCreate, OrderUpdate
from fastapi import HTTPException, status

def get_order_by_id(db: Session, order_id: str) -> Order:
    """Retrieve an order by ID."""
    return db.query(Order).filter(Order.id == order_id).first()

def create_order(db: Session, order: OrderCreate) -> Order:
    """Create a new order with details."""
    db_order = Order(**order.dict(exclude={"details"}))
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    for detail in order.details:
        db_detail = OrderDetail(order_id=db_order.id, **detail.dict())
        db.add(db_detail)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order_id: str, order_update: OrderUpdate) -> Order:
    """Update an existing order with details."""
    db_order = get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail={"errCode": 404, "errMsg": "Order not found"})
    update_data = order_update.dict(exclude_unset=True, exclude={"details"})
    for key, value in update_data.items():
        setattr(db_order, key, value)
    if order_update.details is not None:
        db.query(OrderDetail).filter(OrderDetail.order_id == order_id).delete()
        for detail in order_update.details:
            db_detail = OrderDetail(order_id=order_id, **detail.dict(exclude_unset=True))
            db.add(db_detail)
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: str) -> None:
    """Delete an order and its details."""
    db_order = get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail={"errCode": 404, "errMsg": "Order not found"})
    db.query(OrderDetail).filter(OrderDetail.order_id == order_id).delete()
    db.delete(db_order)
    db.commit()