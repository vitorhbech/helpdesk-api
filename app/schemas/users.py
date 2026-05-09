from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

class UseCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True}