from fastapi import APIRouter, Depends, HTTPException, status

from core.repositories.user import UserRepository
from core.api.v1.schemas.user import (
    UserCreateRequestSchema,
    UserResponseSchema,
)

router = APIRouter(prefix="/register", tags=["Регистрация пользователя"])


@router.post("", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreateRequestSchema, repo: UserRepository = Depends()):
    existing = await repo.get_by_name(user.name)
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = await repo.create(user)
    return db_user
