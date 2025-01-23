from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    user = "user"
    supervisor = "supervisor"
    admin = "admin"

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    rank: Optional[str] = None
    unit: Optional[str] = None
    position: Optional[str] = None
    role: Optional[UserRole] = UserRole.user

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int

    class Config:
        from_attributes = True 