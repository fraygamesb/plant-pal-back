import jwt

from core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.AuthJWT.private_key_path.read_text(),
    algorithm: str = settings.AuthJWT.algorithm,
):
    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.AuthJWT.public_key_path.read_text(),
    algorithm: str = settings.AuthJWT.algorithm,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded
