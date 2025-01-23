from typing import Optional, List
from sqlalchemy import Column, String, Enum
import uuid
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users import schemas
from database import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from models.grievance import Grievance
import enum

class UserRole(enum.Enum):
    user = "user"
    supervisor = "supervisor"
    admin = "admin"

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    service_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    rank: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    unit: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    position: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.user)
    grievances: Mapped[List["Grievance"]] = relationship("Grievance", back_populates="user")

    def to_dict(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "name": self.name,
            "service_number": self.service_number,
            "rank": self.rank,
            "unit": self.unit,
            "position": self.position,
            "phone": self.phone,
            "role": self.role.value if self.role else None
        }

class UserRead(schemas.BaseUser[uuid.UUID]):
    name: Optional[str] = None
    service_number: Optional[str] = None
    rank: Optional[str] = None
    unit: Optional[str] = None
    position: Optional[str] = None
    phone: Optional[str] = None
    role: str
    
    class Config:
        from_attributes = True

class UserCreate(schemas.BaseUserCreate):
    role: str = "user"

class UserUpdate(schemas.BaseUserUpdate):
    name: Optional[str] = None
    service_number: Optional[str] = None
    rank: Optional[str] = None
    unit: Optional[str] = None
    position: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None 