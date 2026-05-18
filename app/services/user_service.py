from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from fastapi import HTTPException, status
from uuid import UUID
from typing import cast

def get_user_by_email(db: Session, email: str) -> User | None:
    """Retrieve a user by email."""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user."""
    hashed = hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_users(db: Session) -> list[User]:
    """Retrieve all users in the system (Admin Only)."""
    return db.query(User).all()

def update_user_role(db: Session, user_id: UUID, new_role: str) -> User:
    """Update the role of a specific user (Admin Only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if new_role not in ["admin", "agent", "customer"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Must be 'admin', 'agent', or 'customer'."
        )
    
    user.role = new_role
    db.commit()
    db.refresh(user)
    return user