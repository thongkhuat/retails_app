# api/v1/inventory.py
"""Inventory API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.inventory import InventoryCreate, InventoryOut, InventoryUpdate
from crud.inventory import create_inventory, update_inventory, delete_inventory
from api.deps import get_db_session, get_current_active_user
from models.db_models import User

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.post("/", response_model=InventoryOut)
async def create_new_inventory(inventory: InventoryCreate, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_active_user)):
    """Create a new inventory record."""
    return create_inventory(db, inventory)

@router.put("/{inventory_id}", response_model=InventoryOut)
async def update_existing_inventory(inventory_id: str, inventory: InventoryUpdate, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_active_user)):
    """Update an inventory record by ID."""
    return update_inventory(db, inventory_id, inventory)

@router.delete("/{inventory_id}")
async def remove_inventory(inventory_id: str, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_active_user)):
    """Delete an inventory record by ID."""
    delete_inventory(db, inventory_id)
    return {"message": "Inventory deleted"}