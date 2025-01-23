from fastapi import Depends, HTTPException, status
from auth.users import current_user
from models.user import User, UserRole

async def get_user_admin(user: User = Depends(current_user)):
    if user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user

async def get_user_supervisor(user: User = Depends(current_user)):
    if user.role not in [UserRole.supervisor, UserRole.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Supervisor or admin access required"
        )
    return user 