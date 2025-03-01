# crud/product.py
"""CRUD operations for Product model."""

from sqlalchemy.orm import Session
from models.db_models import Product
from schemas.product import ProductCreate, ProductUpdate
from fastapi import HTTPException, status

def get_product_by_id(db: Session, product_id: str) -> Product:
    """Retrieve a product by ID."""
    return db.query(Product).filter(Product.id == product_id).first()

def search_products(db: Session, keyword: str) -> list[Product]:
    """Search products by name (contains)."""
    return db.query(Product).filter(Product.name.ilike(f"%{keyword}%")).all()

def create_product(db: Session, product: ProductCreate) -> Product:
    """Create a new product."""
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: str, product_update: ProductUpdate) -> Product:
    """Update an existing product."""
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail={"errCode": 404, "errMsg": "Product not found"})
    update_data = product_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: str) -> None:
    """Delete a product."""
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail={"errCode": 404, "errMsg": "Product not found"})
    db.delete(db_product)
    db.commit()