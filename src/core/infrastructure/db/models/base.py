from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __abstract__ = True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"