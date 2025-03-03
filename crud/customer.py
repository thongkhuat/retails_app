# crud/customer.py
"""CRUD operations for Customer model."""

from sqlalchemy.orm import Session
from models.db_models import Customer
from schemas.customer import CustomerCreate, CustomerUpdate
from fastapi import HTTPException
from core.auth_utils import get_password_hash

def get_customer_by_id(db: Session, customer_id: str) -> Customer:
    """Retrieve a customer by ID."""
    return db.query(Customer).filter(Customer.id == customer_id).first()

def search_customers(db: Session, keyword: str) -> list[Customer]:
    """Search customers by first name (contains)."""
    return db.query(Customer).filter(Customer.first_name.ilike(f"%{keyword}%")).all()

def create_customer(db: Session, customer: CustomerCreate) -> Customer:
    """Create a new customer."""
    if db.query(Customer).filter(Customer.email == customer.email).first():
        raise HTTPException(status_code=400, detail={"errCode": 400, "errMsg": "Email already exists"})
    hashed_password = get_password_hash(customer.password)
    db_customer = Customer(**customer.dict(exclude={"password"}), hashed_password=hashed_password)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: str, customer_update: CustomerUpdate) -> Customer:
    """Update an existing customer."""
    db_customer = get_customer_by_id(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail={"errCode": 404, "errMsg": "Customer not found"})
    update_data = customer_update.dict(exclude_unset=True)
    if "email" in update_data and db.query(Customer).filter(Customer.email == update_data["email"], Customer.id != customer_id).first():
        raise HTTPException(status_code=400, detail={"errCode": 400, "errMsg": "Email already exists"})
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data["password"])
        del update_data["password"]
    for key, value in update_data.items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: str) -> None:
    """Delete a customer."""
    db_customer = get_customer_by_id(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail={"errCode": 404, "errMsg": "Customer not found"})
    db.delete(db_customer)
    db.commit()