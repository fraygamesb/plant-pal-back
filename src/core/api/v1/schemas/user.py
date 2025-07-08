import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr
    created_at: datetime = datetime.now()
    # phone_number: str


class UserCreateRequestSchema(UserBaseSchema):
    password: bytes


class UserUpdateRequestSchema(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    # phone_number: str | None = None


class UserResponseSchema(UserBaseSchema):
    id: uuid.UUID
    is_active: bool
