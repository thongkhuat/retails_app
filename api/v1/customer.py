# api/v1/customer.py
"""Customer API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.customer import CustomerCreate, CustomerOut, CustomerUpdate
from crud.customer import get_customer_by_id, search_customers, create_customer, update_customer, delete_customer
from api.deps import get_current_active_user
from core.database import get_db  # Import get_db directly
from models.db_models import User

router = APIRouter(prefix="/customer", tags=["customers"])

@router.get("/{customer_id}", response_model=CustomerOut)
async def read_customer(customer_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Retrieve a customer by ID."""
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail={"errCode": 404, "errMsg": "Customer not found"})
    return customer

@router.get("/", response_model=list[CustomerOut])
async def search_all_customers(keyword: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Search customers by first name."""
    return search_customers(db, keyword)

@router.post("/", response_model=CustomerOut)
async def create_new_customer(customer: CustomerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Create a new customer."""
    return create_customer(db, customer)

@router.put("/{customer_id}", response_model=CustomerOut)
async def update_existing_customer(customer_id: str, customer: CustomerUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Update a customer by ID."""
    return update_customer(db, customer_id, customer)

@router.delete("/{customer_id}")
async def remove_customer(customer_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Delete a customer by ID."""
    delete_customer(db, customer_id)
    return {"message": "Customer deleted"}