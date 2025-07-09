from pathlib import Path

from pydantic import BaseModel


class TokenInfoSchema(BaseModel):
    access_token: str
    token_type: str


class AuthJWT(BaseModel):
    private_key_path: Path = (
        Path(__file__).resolve().parent.parent.parent.parent.parent.parent
        / "certs"
        / "private.pem"
    )
    public_key_path: Path = (
        Path(__file__).resolve().parent.parent.parent.parent.parent.parent
        / "certs"
        / "public.pem"
    )
    algorithm: str = "RS256"
