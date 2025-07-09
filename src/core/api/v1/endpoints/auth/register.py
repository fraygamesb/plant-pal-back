from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.core.repositories.user import UserRepository
from src.core.api.v1.schemas.user import (
    UserCreateRequestSchema,
    UserUpdateRequestSchema,
    UserResponseSchema,
)
from src.core.infrastructure.db.db import database

router = APIRouter(prefix="/register", tags=["Регистрация пользователя"])


@router.post("", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreateRequestSchema, repo: UserRepository = Depends()):
    existing = await repo.get_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = await repo.create(user)
    return db_user
