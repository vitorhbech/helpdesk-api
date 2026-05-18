from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.api.deps import get_db, get_current_user, require_roles
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketResponse
from app.services.ticket_service import (
    create_ticket, get_tickets, get_ticket_by_id,
    update_ticket, delete_ticket
)

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create(data: TicketCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_ticket(db, data, current_user)

@router.get("", response_model=list[TicketResponse])
def list_tickets(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_tickets(db, current_user)

@router.get("/{ticket_id}", response_model=TicketResponse)
def detail(ticket_id: UUID, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_ticket_by_id(db, ticket_id, current_user)

@router.patch("/{ticket_id}", response_model=TicketResponse)
def update(ticket_id: UUID, data: TicketUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return update_ticket(db, ticket_id, data, current_user)

@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(ticket_id: UUID, db: Session = Depends(get_db), current_user=Depends(require_roles("admin"))):
    delete_ticket(db, ticket_id, current_user)