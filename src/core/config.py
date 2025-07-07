from pathlib import Path

from pydantic import SecretStr, PostgresDsn, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from src.core.api.v1.schemas.jwt import AuthJWT


class DBSettings(BaseSettings):
    db_name: str
    db_user: str
    db_password: SecretStr
    db_host: str
    db_port: int
    db_echo: bool
    db_url: PostgresDsn | None = None

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
        if not self.db_url:
            self.db_url = PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.db_user,
                password=self.db_password.get_secret_value(),
                host=self.db_host,
                port=self.db_port,
                path=self.db_name,
            )


class Settings(BaseSettings):
    db_settings: DBSettings = DBSettings()
    BASE_DIR: Path = Path(__file__).resolve().parent
    AuthJWT: AuthJWT = AuthJWT()


settings = Settings()
