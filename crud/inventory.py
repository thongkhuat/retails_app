# crud/inventory.py
"""CRUD operations for Inventory model."""

from sqlalchemy.orm import Session
from models.db_models import Inventory
from schemas.inventory import InventoryCreate, InventoryUpdate
from fastapi import HTTPException, status

def get_inventory_by_id(db: Session, inventory_id: str) -> Inventory:
    """Retrieve an inventory record by ID."""
    return db.query(Inventory).filter(Inventory.id == inventory_id).first()

def create_inventory(db: Session, inventory: InventoryCreate) -> Inventory:
    """Create a new inventory record."""
    db_inventory = Inventory(**inventory.dict())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def update_inventory(db: Session, inventory_id: str, inventory_update: InventoryUpdate) -> Inventory:
    """Update an existing inventory record."""
    db_inventory = get_inventory_by_id(db, inventory_id)
    if not db_inventory:
        raise HTTPException(status_code=404, detail={"errCode": 404, "errMsg": "Inventory not found"})
    update_data = inventory_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_inventory, key, value)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def delete_inventory(db: Session, inventory_id: str) -> None:
    """Delete an inventory record."""
    db_inventory = get_inventory_by_id(db, inventory_id)
    if not db_inventory:
        raise HTTPException(status_code=404, detail={"errCode": 404, "errMsg": "Inventory not found"})
    db.delete(db_inventory)
    db.commit()