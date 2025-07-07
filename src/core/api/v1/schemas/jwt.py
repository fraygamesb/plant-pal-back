from pydantic.v1 import BaseModel
from src.core.config import settings


class AuthJWT(BaseModel):
    private_key_path: str = settings.BASE_DIR.parent / "certs" / "private.pem"
    public_key_path: str = settings.BASE_DIR.parent / "certs" / "public.pem"
    algorithm: str = "RS256"
