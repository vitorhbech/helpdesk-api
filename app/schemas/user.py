from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
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
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdateRole(BaseModel):
    role: str