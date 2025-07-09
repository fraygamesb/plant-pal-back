from pathlib import Path

from pydantic import SecretStr, PostgresDsn, BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from src.core.api.v1.schemas.jwt import AuthJWT


class DBSettings(BaseSettings):
    POSTGRES_DB_NAME: str
    POSTGRES_DB_USER: str
    POSTGRES_DB_PASSWORD: SecretStr
    POSTGRES_DB_HOST: str
    POSTGRES_DB_PORT: int
    POSTGRES_DB_ECHO: bool
    POSTGRES_DB_URL: PostgresDsn | None = None

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            ".env",
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.POSTGRES_DB_URL:
            self.POSTGRES_DB_URL = PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.POSTGRES_DB_USER,
                password=self.POSTGRES_DB_PASSWORD.get_secret_value(),
                host=self.POSTGRES_DB_HOST,
                port=self.POSTGRES_DB_PORT,
                path=self.POSTGRES_DB_NAME,
            )


class Settings(BaseSettings):
    db_settings: DBSettings = DBSettings()
    auth_jwt_settings: AuthJWT = AuthJWT()


settings = Settings()
