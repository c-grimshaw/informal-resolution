from pydantic import BaseModel, UUID4
from datetime import datetime
import uuid
from typing import Optional, List
from models.grievance import GrievanceStatus

class NoteCreate(BaseModel):
    content: str

class NoteRead(BaseModel):
    id: UUID4
    content: str
    created_at: datetime
    user_id: UUID4
    grievance_id: UUID4
    user_name: str  # We'll populate this from the user relationship

    class Config:
        from_attributes = True

class GrievanceBase(BaseModel):
    submitter_name: str
    service_number: str
    rank: str
    email: str
    phone: str
    unit: str
    position: str
    grievance_type: str
    grievance_subtype: str
    description: str
    redress_sought: str
    status: str = "pending"
    title: str

class GrievanceCreate(BaseModel):
    title: str
    description: str
    redress_sought: str
    submitter_name: str
    service_number: str
    rank: str
    email: str
    phone: str
    unit: str
    position: str
    grievance_type: str
    grievance_subtype: str

class GrievanceUpdate(BaseModel):
    submitter_name: Optional[str] = None
    service_number: Optional[str] = None
    rank: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    unit: Optional[str] = None
    position: Optional[str] = None
    grievance_type: Optional[str] = None
    grievance_subtype: Optional[str] = None
    description: Optional[str] = None
    redress_sought: Optional[str] = None
    status: Optional[GrievanceStatus] = None
    title: Optional[str] = None

class GrievanceRead(BaseModel):
    id: UUID4
    title: str
    description: str
    redress_sought: str
    status: GrievanceStatus
    submitter_name: str
    service_number: str
    rank: str
    email: str
    phone: str
    unit: str
    position: str
    grievance_type: str
    grievance_subtype: str
    created_at: datetime
    user_id: UUID4
    notes: List[NoteRead] = []

    class Config:
        from_attributes = True 