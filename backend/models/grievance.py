from datetime import datetime, UTC
from sqlalchemy import String, DateTime, ForeignKey, Column, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid
import enum
from typing import List, Optional

class GrievanceStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    resolved = "resolved"

class Note(Base):
    __tablename__ = "notes"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    grievance_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("grievance.id", ondelete="CASCADE"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    
    # Relationships
    grievance: Mapped["Grievance"] = relationship("Grievance", back_populates="notes")
    user: Mapped["User"] = relationship("User")

class Grievance(Base):
    __tablename__ = "grievance"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Personal Information
    submitter_name: Mapped[str] = mapped_column(String(length=200))
    service_number: Mapped[str] = mapped_column(String(length=50))
    rank: Mapped[str] = mapped_column(String(length=50))
    email: Mapped[str] = mapped_column(String(length=200))
    phone: Mapped[str] = mapped_column(String(length=50))
    
    # Unit Details
    unit: Mapped[str] = mapped_column(String(length=100))
    position: Mapped[str] = mapped_column(String(length=200))
    
    # Grievance Details
    title: Mapped[str] = mapped_column(String(length=200))
    grievance_type: Mapped[str] = mapped_column(String(length=100))
    grievance_subtype: Mapped[str] = mapped_column(String(length=100))
    description: Mapped[str] = mapped_column(String(length=2000))
    redress_sought: Mapped[str] = mapped_column(String(length=1000))
    
    # Metadata
    status: Mapped[GrievanceStatus] = mapped_column(Enum(GrievanceStatus), default=GrievanceStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    
    # Foreign key to user
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="grievances")
    notes: Mapped[List["Note"]] = relationship("Note", back_populates="grievance", cascade="all, delete-orphan", order_by=Note.created_at.desc()) 