from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketUpdate
from typing import cast
from uuid import UUID
from typing import cast, Any

def get_tickets(db: Session, current_user: User) -> list[Ticket]:
    # Return tickets visible to the current user
    if str(current_user.role) == "admin":
        return db.query(Ticket).all()

    user_id = cast(UUID, current_user.id)

    if str(current_user.role) == "customer":
        return db.query(Ticket).filter(Ticket.created_by == user_id).all()

    if str(current_user.role) == "agent":
        # Agents can see tickets they created or are assigned to
        return db.query(Ticket).filter(
            or_(Ticket.created_by == user_id, Ticket.assigned_to == user_id)
        ).all()

    # Fallback: no tickets
    return []

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

    ticket_creator_id = cast(UUID, ticket.created_by)
    ticket_assignee_id = cast(UUID | None, ticket.assigned_to)
    user_id = cast(UUID, current_user.id)


    if current_user.role == "customer":
        if ticket_creator_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
    if current_user.role == "agent":
        is_creator = ticket_creator_id == user_id
        is_assignee = ticket_assignee_id == user_id
        if not (is_creator or is_assignee):
            raise HTTPException(status_code=403, detail="Access denied")
        
    return ticket

def update_ticket(db: Session, ticket_id: UUID, data: TicketUpdate, current_user: User) -> Ticket:

    ticket = get_ticket(db, ticket_id, current_user)
    
    update_data = data.model_dump(exclude_unset=True)
    
    if "status" in update_data:
        current_status = str(ticket.status)
        new_status = str(update_data["status"])
        user_role = str(current_user.role)
        
        if current_status != new_status:
            
            if current_status == "closed":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Closed tickets cannot be modified or reopened."
                )
            
            if current_status == "open":
                if new_status == "in_progress" and user_role in ["agent", "admin"]:
                    pass  
                elif new_status == "closed" and user_role == "admin":
                    pass  
                else:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Transition from {current_status} to {new_status} not permitted for role '{user_role}'."
                    )
                    
            elif current_status == "in_progress":
                if new_status == "resolved" and user_role in ["agent", "admin"]:
                    pass  
                else:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Transition from {current_status} to {new_status} not permitted for role '{user_role}'."
                    )
                    
            elif current_status == "resolved":
                if new_status == "closed" and user_role in ["customer", "agent", "admin"]:
                    pass  
                elif new_status == "open" and user_role in ["customer", "admin"]:
                    pass  
                else:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Transition from {current_status} to {new_status} not permitted for role '{user_role}'."
                    )
            else:
                # Caso caia em algum status não mapeado
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid ticket status workflow."
                )

    # Aplica as atualizações validadas no objeto do banco
    for key, value in update_data.items():
        setattr(ticket, key, value)
    
    db.commit()
    db.refresh(ticket)
    return ticket

def assign_ticket(db: Session, ticket_id: UUID, agent_id: UUID, current_user: User) -> Ticket:
    """Assign a ticket to a specific agent (Admin/Agent Only)."""

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    target_user = db.query(User).filter(User.id == agent_id).first()

    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target user not found."
        )
    
    if str(target_user.role) not in ["agent", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tickets can only be assigned to users with 'agent' or 'admin' roles."
        )
    
    setattr(ticket, "assigned_to", cast(Any, agent_id))

    
    db.commit()
    db.refresh(ticket)
    return ticket