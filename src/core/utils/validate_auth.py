from fastapi import Depends, HTTPException, Form
from starlette import status
from fastapi.security import OAuth2PasswordBearer

from core.api.v1.schemas.user import UserResponseSchema
from core.utils import auth
from core.repositories.user import UserRepository
from core.utils.security import verify_password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login/")


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    payload = auth.decode_jwt(
        token=token,
    )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    repo: UserRepository = Depends(),
) -> UserResponseSchema:
    username: str = payload.get("name")
    user = await repo.get_by_username(username)
    if user:
        return UserResponseSchema(
            id=user.id,
            email=user.email,
            name=user.name,
        )
    raise HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="token invalid",
    )


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    repo: UserRepository = Depends(),
) -> UserResponseSchema:
    user = await repo.get_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not verify_password(password, user.password.encode()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )
    return UserResponseSchema(
        id=user.id,
        email=user.email,
        name=user.name,
    )
