# api/v1/product.py
"""Product API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.product import ProductCreate, ProductOut, ProductUpdate
from crud.product import get_product_by_id, search_products, create_product, update_product, delete_product
from api.deps import get_db_session, get_current_active_user
from models.db_models import User

router = APIRouter(prefix="/product", tags=["products"])

@router.get("/{product_id}", response_model=ProductOut)
async def read_product(product_id: str, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_active_user)):
    """Retrieve a product by ID."""
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail={"errCode": 404, "errMsg": "Product not found"})
    return product

@router.get("/", response_model=list[ProductOut])
async def search_all_products(keyword: str, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_active_user)):
    """Search products by name."""
    return search_products(db, keyword)

@router.post("/", response_model=ProductOut)
async def create_new_product(product: ProductCreate, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_active_user)):
    """Create a new product."""
    return create_product(db, product)

@router.put("/{product_id}", response_model=ProductOut)
async def update_existing_product(product_id: str, product: ProductUpdate, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_active_user)):
    """Update a product by ID."""
    return update_product(db, product_id, product)

@router.delete("/{product_id}")
async def remove_product(product_id: str, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_active_user)):
    """Delete a product by ID."""
    delete_product(db, product_id)
    return {"message": "Product deleted"}