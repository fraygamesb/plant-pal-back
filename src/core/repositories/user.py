import uuid

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from core.infrastructure.db.models.user import User
from core.infrastructure.db.db import database
from core.api.v1.schemas.user import (
    UserCreateRequestSchema,
    UserUpdateRequestSchema,
)
from core.utils.security import hash_password
from datetime import datetime


class UserRepository:
    def __init__(
        self, session: AsyncSession = Depends(database.scoped_session_dependency)
    ) -> None:
        self.session = session
        self.model = User

    async def get_by_id(self, id: str) -> User | None:
        result = await self.session.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> User | None:
        result = await self.session.execute(select(User).where(User.name == name))
        return result.scalar_one_or_none()

    async def create(self, user: UserCreateRequestSchema) -> User:
        user = User(
            id=uuid.uuid4(),
            name=user.name,
            email=user.email,
            password=hash_password(
                user.password.decode()
                if isinstance(user.password, bytes)
                else user.password
            ).decode(),
            is_active=True,
            created_at=datetime.utcnow(),
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(
        self, user_id: uuid.UUID, user_data: UserUpdateRequestSchema
    ) -> User | None:
        user = await self.get_by_id(str(user_id))
        if not user:
            return None

        update_data = {}

        if user_data.name is not None:
            update_data["name"] = user_data.name

        if user_data.email is not None:
            update_data["email"] = user_data.email

        if user_data.password is not None:
            update_data["password"] = hash_password(user_data.password).decode()

        if update_data:
            await self.session.execute(
                update(User).where(User.id == user_id).values(**update_data)
            )
            await self.session.commit()

            await self.session.refresh(user)

        return user

    async def delete(self, user_id: uuid.UUID) -> bool:
        user = await self.get_by_id(str(user_id))
        if not user:
            return False

        await self.session.execute(delete(User).where(User.id == user_id))
        await self.session.commit()

        return True

    async def deactivate(self, user_id: uuid.UUID) -> bool:
        user = await self.get_by_id(str(user_id))
        if not user:
            return False

        await self.session.execute(
            update(User).where(User.id == user_id).values(is_active=False)
        )
        await self.session.commit()

        return True

    async def activate(self, user_id: uuid.UUID) -> bool:
        user = await self.get_by_id(str(user_id))
        if not user:
            return False

        await self.session.execute(
            update(User).where(User.id == user_id).values(is_active=True)
        )
        await self.session.commit()

        return True
