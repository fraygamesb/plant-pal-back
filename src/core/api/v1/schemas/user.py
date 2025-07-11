import uuid

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr
from typing import Annotated


class UserBaseSchema(BaseModel):
    name: Annotated[str, MinLen(3), MaxLen(20)]
    email: Annotated[str, EmailStr]
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


class UserLoginRequestSchema(BaseModel):
    email: Annotated[str, EmailStr]
    password: str
