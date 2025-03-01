# main.py
"""Main entry point for the FastAPI application."""

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from core.database import Base, engine, get_db
from core.security import create_access_token, get_current_user
from core.auth_utils import verify_password
from crud.user import get_user_by_username, create_user
from schemas.user import UserCreate
from models.db_models import User
from api.v1 import user, customer, product, inventory, order
from core.config import settings

app = FastAPI(title="Retail App Service")

# Include API routers
app.include_router(user.router)
app.include_router(customer.router)
app.include_router(product.router)
app.include_router(inventory.router)
app.include_router(order.router)

# Create database tables
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup_event():
    """Initialize the superuser on app startup."""
    db = next(get_db())
    if not get_user_by_username(db, "admin"):
        admin = UserCreate(
            username="admin",
            password="12345678",
            email="admin@example.com",
            role="admin",
        )
        user = create_user(db, admin)
        user.is_superuser = True
        db.commit()

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"errCode": 401, "errMsg": "Incorrect username or password"},
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/logout/{username}")
async def logout(username: str, current_user: User = Depends(get_current_user)):
    """Logout user (client-side token discard)."""
    if current_user.username != username:
        raise HTTPException(status_code=403, detail={"errCode": 403, "errMsg": "Forbidden"})
    return {"message": "Logged out successfully"}

# Custom error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors."""
    return {"errCode": 404, "errMsg": "Not Found"}

@app.exception_handler(403)
async def forbidden_handler(request, exc):
    """Handle 403 errors."""
    return {"errCode": 403, "errMsg": "Forbidden"}