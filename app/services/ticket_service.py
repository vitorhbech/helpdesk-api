from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketUpdate
from uuid import UUID

def get_tickets(db: Session, current_user: User) -> list[Ticket]:
    if current_user.role == "admin":
        return db.query(Ticket).all()
    elif current_user.role == "agent":
        return db.query(Ticket).filter(
            or_(
                Ticket.created_by == current_user.id, 
                Ticket.assigned_to == current_user.id
            )
        ).all()
    else:
        return db.query(Ticket).filter(Ticket.created_by == current_user.id).all()

def create_ticket(db: Session, ticket: TicketCreate, current_user: User) -> Ticket:
    db_ticket = Ticket(**ticket.model_dump(), created_by=current_user.id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_ticket(db: Session, ticket_id: UUID, current_user: User) -> Ticket:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Validação de acesso
    if current_user.role == "customer" and ticket.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
        
    return ticket

def update_ticket(db: Session, ticket_id: UUID, data: TicketUpdate, current_user: User) -> Ticket:
    ticket = get_ticket(db, ticket_id, current_user)
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ticket, key, value)
    
    db.commit()
    db.refresh(ticket)
    return ticket