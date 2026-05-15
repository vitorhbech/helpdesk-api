from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

class TicketCreate(BaseModel):
    title: str
    description: str
    priority: Optional[str] = "low"

class TicketUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[UUID] = None

class TicketResponse(BaseModel):
    id: UUID
    title: str
    description: str
    status: str
    priority: str
    created_by: UUID
    assigned_to: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

model_config = {
    "from_attributes": True,}