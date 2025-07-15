import uuid
from datetime import datetime, timedelta

import jwt

from core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.PRIVATE_KEY_PATH.read_text(),
    algorithm: str = "RS256",
    expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = datetime.utcnow() + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
        jti=str(uuid.uuid4()),
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.PUBLIC_KEY_PATH.read_text(),
    algorithm: str = "RS256",
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded
