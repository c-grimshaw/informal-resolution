from typing import Optional, Union
from fastapi import Depends, Request, HTTPException
from fastapi_users import BaseUserManager, UUIDIDMixin
import uuid
from models.user import User, UserCreate
from auth.users import current_user

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = "SECRET-RESET-TOKEN"
    verification_token_secret = "SECRET-VERIFY-TOKEN"

    async def validate_password(self, password: str, user: Union[UserCreate, User]) -> None:
        await super().validate_password(password, user)
        
    async def create(
        self,
        user_create: UserCreate,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> User:
        # Get current user from request if available
        current_user_instance = None
        if request:
            try:
                current_user_instance = await current_user(request)
            except Exception:
                current_user_instance = None

        # Validate role permissions
        requested_role = user_create.role
        if requested_role == "admin":
            if not current_user_instance or current_user_instance.role != "admin":
                raise HTTPException(
                    status_code=403,
                    detail="Only admins can create admin accounts"
                )
        elif requested_role == "supervisor":
            if not current_user_instance or current_user_instance.role not in ["admin", "supervisor"]:
                raise HTTPException(
                    status_code=403,
                    detail="Only supervisors and admins can create supervisor accounts"
                )

        return await super().create(user_create, safe, request)

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered with role {user.role}") 