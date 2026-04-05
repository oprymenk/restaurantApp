from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    role: str = "user"  # user, manager, admin, courier, kitchen

class UserCreate(UserBase):
    password: str

class UserDB(UserBase):
    id: str = Field(default_factory=str, alias="_id")
    created_at: datetime