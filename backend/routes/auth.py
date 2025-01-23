from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import uuid
from models.user import User, UserRead, UserCreate, UserUpdate, UserRole
from auth.users import fastapi_users, current_user
from auth.auth import auth_backend
from auth.dependencies import get_user_admin, get_user_supervisor
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

auth_router = APIRouter(tags=["auth"])
users_router = APIRouter(tags=["users"])

# Add our custom endpoints first
@users_router.get("/all", response_model=List[UserRead])
async def get_all_users(
    user: User = Depends(get_user_supervisor),
    db: AsyncSession = Depends(get_async_session)
):
    """Get all users. Only accessible by supervisors and admins."""
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [UserRead.model_validate(user) for user in users]

@users_router.patch("/me", response_model=UserRead)
async def update_own_profile(
    user_update: UserUpdate,
    current_user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """Update the current user's profile. Accessible by any authenticated user."""
    # Get the current user
    result = await db.execute(select(User).where(User.id == current_user.id))
    user_to_update = result.scalar_one_or_none()
    
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update fields, excluding role changes
    update_data = user_update.model_dump(exclude_unset=True)
    if "role" in update_data:
        del update_data["role"]  # Users cannot change their own role
    
    for field, value in update_data.items():
        setattr(user_to_update, field, value)
    
    await db.commit()
    await db.refresh(user_to_update)
    
    return user_to_update

@users_router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: uuid.UUID,
    user_update: UserUpdate,
    current_user: User = Depends(get_user_admin),  # Only admins can update roles
    db: AsyncSession = Depends(get_async_session)
):
    """Update any user. Only accessible by admins."""
    print(f"Update user request - User ID: {user_id}, Current user role: {current_user.role}")
    print(f"Update data: {user_update.model_dump()}")
    
    # Get the user to update
    result = await db.execute(select(User).where(User.id == user_id))
    user_to_update = result.scalar_one_or_none()
    
    if not user_to_update:
        print(f"User {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update fields
    update_data = user_update.model_dump(exclude_unset=True)
    print(f"Processed update data: {update_data}")
    
    # Special handling for role updates
    if "role" in update_data:
        new_role = update_data["role"]
        print(f"Role update requested: {new_role}")
        # Validate role value
        if new_role not in ["user", "supervisor", "admin"]:
            print(f"Invalid role value: {new_role}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role"
            )
    
    for field, value in update_data.items():
        setattr(user_to_update, field, value)
    
    try:
        await db.commit()
        await db.refresh(user_to_update)
        print(f"User {user_id} updated successfully with new role: {user_to_update.role}")
        return user_to_update
    except Exception as e:
        print(f"Error updating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Then include FastAPI Users routes
auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
)

auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
)

# Get the users router but exclude the PATCH route
user_router = fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=False)
for route in user_router.routes:
    if route.methods != {"PATCH"}:  # Include all routes except PATCH
        users_router.routes.append(route)

@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: uuid.UUID,
    user: User = Depends(get_user_admin)  # Only admins
):
    """Delete a user. Only accessible by admins."""
    try:
        await fastapi_users.delete(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
