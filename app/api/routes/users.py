from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.deps import get_db, require_roles
from app.schemas.user import UserResponse, UserUpdateRole
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("admin")) 
):
    """List all users in the system (Admin Only)."""
    return user_service.get_all_users(db)

@router.patch("/{user_id}/role", response_model=UserResponse)
def change_user_role(
    user_id: UUID,
    data: UserUpdateRole,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("admin"))
):
    """Update a user's role (Admin Only)."""
    return user_service.update_user_role(db, user_id=user_id, new_role=data.role)