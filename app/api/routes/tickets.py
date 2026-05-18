from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.deps import get_db, require_roles
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketResponse
from app.services.ticket_service import (
    create_ticket, 
    get_tickets, 
    get_ticket,       
    update_ticket
)

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: TicketCreate, 
    db: Session = Depends(get_db), 
    current_user = Depends(require_roles("admin", "agent", "customer"))
):
    return create_ticket(db, data, current_user)

@router.get("", response_model=list[TicketResponse])
def list_tickets(
    db: Session = Depends(get_db), 
    current_user = Depends(require_roles("admin", "agent", "customer"))
):
    return get_tickets(db, current_user)

@router.get("/{ticket_id}", response_model=TicketResponse)
def detail(
    ticket_id: UUID, 
    db: Session = Depends(get_db), 
    current_user = Depends(require_roles("admin", "agent", "customer"))
):
    return get_ticket(db, ticket_id, current_user)

@router.patch("/{ticket_id}", response_model=TicketResponse)
def update(
    ticket_id: UUID, 
    data: TicketUpdate, 
    db: Session = Depends(get_db), 
    current_user = Depends(require_roles("admin", "agent", "customer"))
):
    return update_ticket(db, ticket_id, data, current_user)

#  Delete endpoint is currently disabled to prevent accidental data loss. It can be re-enabled in the future if needed.
# @router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete(
#     ticket_id: UUID, 
#     db: Session = Depends(get_db), 
#     current_user = Depends(require_roles("admin"))
# ):
#     delete_ticket(db, ticket_id, current_user)