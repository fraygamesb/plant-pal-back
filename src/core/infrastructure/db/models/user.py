import uuid

from pydantic.v1 import EmailStr
from sqlalchemy import String, Text, DateTime, func, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)

    name: Mapped[str]
    email: Mapped[EmailStr]
    password: Mapped[str]
    phone_number: Mapped[str]
    is_active: Mapped[bool] = False
