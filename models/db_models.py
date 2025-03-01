# models/db_models.py
"""SQLAlchemy database models with UUID IDs."""

from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
import uuid
from core.database import Base

class User(Base):
    """User model for authentication and roles."""
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

class Customer(Base):
    """Customer model for retail transactions."""
    __tablename__ = "customers"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    dob = Column(DateTime)
    last_purchase_order_id = Column(String)
    last_activity_time = Column(DateTime, default=func.now())
    address = Column(String)
    email = Column(String, nullable=False, unique=True)

class Product(Base):
    """Product model for items sold."""
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    type = Column(String, nullable=False, index=True)
    created_date = Column(DateTime, nullable=False)
    retail_price = Column(Float, nullable=False)
    remark = Column(String)

class Inventory(Base):
    """Inventory model for stock tracking."""
    __tablename__ = "inventories"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    qty = Column(Float, nullable=False)  # Changed to Float for consistency
    type = Column(String, nullable=False)
    source = Column(String)
    destination = Column(String)
    created_time = Column(DateTime, nullable=False)
    created_by = Column(String, nullable=False)
    remark = Column(String)

class Order(Base):
    """Order model for customer purchases."""
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    created_time = Column(DateTime, nullable=False)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    is_delivered = Column(Boolean, nullable=False)
    note = Column(String)
    delivered_time = Column(DateTime)
    total_retail_price = Column(Float)
    total_real_price = Column(Float)

class OrderDetail(Base):
    """OrderDetail model for order items."""
    __tablename__ = "order_details"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    qty = Column(Float, nullable=False)  # Changed to Float for consistency
    discount = Column(Float)
    retail_price = Column(Float)
    real_price = Column(Float)