import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)

    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    is_active: Mapped[bool]
    created_at: Mapped[datetime]
    # phone_number: Mapped[str]
