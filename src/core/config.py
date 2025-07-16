from pathlib import Path

from pydantic import SecretStr, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent.parent / "docker" / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # AuthJWT
    PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / "private.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "public.pem"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # PostgreSQL
    POSTGRES_DB_NAME: str
    POSTGRES_DB_USER: str
    POSTGRES_DB_PASSWORD: SecretStr
    POSTGRES_DB_HOST: str
    POSTGRES_DB_PORT: int = 5432
    POSTGRES_DB_ECHO: bool
    POSTGRES_DB_URL: PostgresDsn | None = None

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


settings = Settings()
