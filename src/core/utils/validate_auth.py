from fastapi import Depends, HTTPException
from starlette import status

from src.core.api.v1.schemas.user import UserLoginRequestSchema
from src.core.infrastructure.db.models import User
from src.core.repositories.user import UserRepository
from src.core.utils.security import verify_password


async def validate_auth_user(
    login_data: UserLoginRequestSchema, repo: UserRepository = Depends()
) -> User:
    user = await repo.get_by_email(login_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not verify_password(login_data.password, user.password.encode()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )
    return user
