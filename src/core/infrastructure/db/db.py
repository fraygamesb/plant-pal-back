from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)

from core.config import settings


class Database:
    def __init__(self, url: str, echo: bool):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    async def scoped_session_dependency(self) -> AsyncGenerator:
        async with self.session_factory() as session:
            yield session
            await session.close()


database = Database(
    url=settings.db_settings.db_url.unicode_string(), echo=settings.db_settings.db_echo
)
