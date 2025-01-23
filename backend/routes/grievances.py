from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid
from database import get_async_session
from models.grievance import Grievance, Note
from models.user import User, UserRole
from schemas.grievance import GrievanceCreate, GrievanceRead, GrievanceUpdate, NoteCreate, NoteRead
from auth.users import current_user
from auth.dependencies import get_user_supervisor
from datetime import datetime

router = APIRouter(prefix="/grievances", tags=["grievances"])

@router.post("", response_model=GrievanceRead)
async def create_grievance(
    grievance: GrievanceCreate,
    current_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    db_grievance = Grievance(
        **grievance.model_dump(),
        user_id=current_user.id
    )
    session.add(db_grievance)
    await session.commit()
    await session.refresh(db_grievance)
    
    # Create a response object without notes
    response = GrievanceRead(
        id=db_grievance.id,
        title=db_grievance.title,
        description=db_grievance.description,
        redress_sought=db_grievance.redress_sought,
        status=db_grievance.status,
        submitter_name=db_grievance.submitter_name,
        service_number=db_grievance.service_number,
        rank=db_grievance.rank,
        email=db_grievance.email,
        phone=db_grievance.phone,
        unit=db_grievance.unit,
        position=db_grievance.position,
        grievance_type=db_grievance.grievance_type,
        grievance_subtype=db_grievance.grievance_subtype,
        created_at=db_grievance.created_at,
        user_id=db_grievance.user_id,
        notes=[]  # New grievance has no notes
    )
    return response

@router.get("", response_model=list[GrievanceRead])
async def read_grievances(
    current_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Grievance)
    
    if current_user.role == UserRole.admin:
        # Admins can see all grievances
        print("DEBUG: User is admin, no filters applied")
        pass
    elif current_user.role == UserRole.supervisor:
        # Supervisors can see their own grievances and grievances from their unit
        print(f"DEBUG: User is supervisor, filtering by unit {current_user.unit}")
        query = query.where((Grievance.user_id == current_user.id) | 
                          (Grievance.unit == current_user.unit))
    else:
        # Regular users can only see their own grievances
        print("DEBUG: User is regular user, filtering by user_id")
        query = query.where(Grievance.user_id == current_user.id)
    
    result = await session.execute(query)
    grievances = result.scalars().all()
    print(f"DEBUG: Found {len(grievances)} grievances")
    
    # Create response objects with empty notes arrays
    response = []
    for grievance in grievances:
        response.append(GrievanceRead(
            id=grievance.id,
            title=grievance.title,
            description=grievance.description,
            redress_sought=grievance.redress_sought,
            status=grievance.status,
            submitter_name=grievance.submitter_name,
            service_number=grievance.service_number,
            rank=grievance.rank,
            email=grievance.email,
            phone=grievance.phone,
            unit=grievance.unit,
            position=grievance.position,
            grievance_type=grievance.grievance_type,
            grievance_subtype=grievance.grievance_subtype,
            created_at=grievance.created_at,
            user_id=grievance.user_id,
            notes=[]  # Initialize with empty notes
        ))
    return response

@router.get("/{grievance_id}", response_model=GrievanceRead)
async def read_grievance(
    grievance_id: uuid.UUID,
    current_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Grievance).where(Grievance.id == grievance_id)
    result = await session.execute(query)
    grievance = result.scalar_one_or_none()
    
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")
    
    # Check permissions
    if current_user.role == UserRole.admin or \
       (current_user.role == UserRole.supervisor and (grievance.unit == current_user.unit or grievance.user_id == current_user.id)) or \
       grievance.user_id == current_user.id:
        
        # Load notes for this grievance
        notes_query = select(Note).where(Note.grievance_id == grievance_id).order_by(Note.created_at.desc())
        notes_result = await session.execute(notes_query)
        notes = notes_result.scalars().all()
        
        # Create note responses with user names
        note_responses = []
        for note in notes:
            user = await session.get(User, note.user_id)
            note_responses.append(NoteRead(
                id=note.id,
                content=note.content,
                created_at=note.created_at,
                user_id=note.user_id,
                grievance_id=note.grievance_id,
                user_name=user.name or user.email
            ))
        
        # Create response with notes
        return GrievanceRead(
            id=grievance.id,
            title=grievance.title,
            description=grievance.description,
            redress_sought=grievance.redress_sought,
            status=grievance.status,
            submitter_name=grievance.submitter_name,
            service_number=grievance.service_number,
            rank=grievance.rank,
            email=grievance.email,
            phone=grievance.phone,
            unit=grievance.unit,
            position=grievance.position,
            grievance_type=grievance.grievance_type,
            grievance_subtype=grievance.grievance_subtype,
            created_at=grievance.created_at,
            user_id=grievance.user_id,
            notes=note_responses
        )
        
    raise HTTPException(status_code=403, detail="Not authorized to access this grievance")

@router.put("/{grievance_id}", response_model=GrievanceRead)
async def update_grievance(
    grievance_id: uuid.UUID,
    grievance_update: GrievanceUpdate,
    current_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Grievance).where(Grievance.id == grievance_id)
    result = await session.execute(query)
    grievance = result.scalar_one_or_none()
    
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")
    
    # Check permissions
    if current_user.role == UserRole.admin:
        pass  # Admins can update any grievance
    elif current_user.role == UserRole.supervisor:
        if not (grievance.unit == current_user.unit or grievance.user_id == current_user.id):
            raise HTTPException(status_code=403, detail="Not authorized to update this grievance")
    elif grievance.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this grievance")
    
    # Update fields
    update_data = grievance_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(grievance, field, value)
    
    await session.commit()
    await session.refresh(grievance)
    
    # Create response object with empty notes array
    response = GrievanceRead(
        id=grievance.id,
        title=grievance.title,
        description=grievance.description,
        redress_sought=grievance.redress_sought,
        status=grievance.status,
        submitter_name=grievance.submitter_name,
        service_number=grievance.service_number,
        rank=grievance.rank,
        email=grievance.email,
        phone=grievance.phone,
        unit=grievance.unit,
        position=grievance.position,
        grievance_type=grievance.grievance_type,
        grievance_subtype=grievance.grievance_subtype,
        created_at=grievance.created_at,
        user_id=grievance.user_id,
        notes=[]  # Initialize with empty notes
    )
    return response

@router.delete("/{grievance_id}")
async def delete_grievance(
    grievance_id: uuid.UUID,
    current_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    # Get the grievance
    query = select(Grievance).where(Grievance.id == grievance_id)
    result = await session.execute(query)
    grievance = result.scalar_one_or_none()
    
    if not grievance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grievance not found"
        )
    
    # Check if user owns the grievance or is admin
    if grievance.user_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this grievance"
        )
    
    await session.delete(grievance)
    await session.commit()
    
    return {"message": "Grievance deleted successfully"}

@router.get("/user/{user_id}", response_model=list[GrievanceRead])
async def read_user_grievances(
    user_id: uuid.UUID,
    current_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    # Check permissions
    if current_user.id != user_id and current_user.role not in [UserRole.admin, UserRole.supervisor]:
        raise HTTPException(status_code=403, detail="Not authorized to view these grievances")
    
    query = select(Grievance).where(Grievance.user_id == user_id)
    result = await session.execute(query)
    grievances = result.scalars().all()
    
    # Create response objects with empty notes arrays
    response = []
    for grievance in grievances:
        response.append(GrievanceRead(
            id=grievance.id,
            title=grievance.title,
            description=grievance.description,
            redress_sought=grievance.redress_sought,
            status=grievance.status,
            submitter_name=grievance.submitter_name,
            service_number=grievance.service_number,
            rank=grievance.rank,
            email=grievance.email,
            phone=grievance.phone,
            unit=grievance.unit,
            position=grievance.position,
            grievance_type=grievance.grievance_type,
            grievance_subtype=grievance.grievance_subtype,
            created_at=grievance.created_at,
            user_id=grievance.user_id,
            notes=[]  # Initialize with empty notes
        ))
    return response

@router.post("/{grievance_id}/notes", response_model=NoteRead)
async def create_note(
    grievance_id: uuid.UUID,
    note: NoteCreate,
    current_user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """Create a new note for a grievance."""
    # Check if grievance exists and user has access
    grievance = await db.get(Grievance, grievance_id)
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")

    db_note = Note(
        content=note.content,
        grievance_id=grievance_id,
        user_id=current_user.id
    )
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    
    # Create response with user name
    response = NoteRead(
        id=db_note.id,
        content=db_note.content,
        created_at=db_note.created_at,
        user_id=db_note.user_id,
        grievance_id=db_note.grievance_id,
        user_name=current_user.name or current_user.email
    )
    return response

@router.get("/{grievance_id}/notes", response_model=List[NoteRead])
async def get_notes(
    grievance_id: uuid.UUID,
    current_user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """Get all notes for a grievance."""
    # Check if grievance exists and user has access
    grievance = await db.get(Grievance, grievance_id)
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")

    result = await db.execute(
        select(Note)
        .where(Note.grievance_id == grievance_id)
        .order_by(Note.created_at.desc())
    )
    notes = result.scalars().all()
    
    # Create response with user names
    response = []
    for note in notes:
        user = await db.get(User, note.user_id)
        response.append(NoteRead(
            id=note.id,
            content=note.content,
            created_at=note.created_at,
            user_id=note.user_id,
            grievance_id=note.grievance_id,
            user_name=user.name or user.email
        ))
    return response 