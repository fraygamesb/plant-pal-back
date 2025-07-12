from fastapi import Depends, HTTPException, Form
from starlette import status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.core.api.v1.schemas.user import UserLoginRequestSchema
from src.core.utils.jwt_helper import (
    ACCESS_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
    REFRESH_TOKEN_TYPE,
)
from src.core.api.v1.schemas.user import UserResponseSchema
from src.core.utils import auth
from src.core.repositories.user import UserRepository
from src.core.utils.security import verify_password


oauth2_scheme = HTTPBearer()


def get_current_token_payload(
    creds: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
) -> dict:
    token = creds.credentials
    payload = auth.decode_jwt(
        token=token,
    )
    return payload


# def get_current_token_payload(
#     token: str = Depends(oauth2_scheme),
# ) -> dict:
#     payload = auth.decode_jwt(
#         token=token,
#     )
#     return payload


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type != token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid token type {current_token_type!r} expected {token_type!r}.",
    )


async def get_user_by_token_sub(
    payload: dict,
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


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    repo: UserRepository = Depends(),
) -> UserResponseSchema:
    validate_token_type(payload, ACCESS_TOKEN_TYPE)
    return await get_user_by_token_sub(payload, repo)


async def get_current_auth_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
    repo: UserRepository = Depends(),
) -> UserResponseSchema:
    validate_token_type(payload, REFRESH_TOKEN_TYPE)
    return await get_user_by_token_sub(payload, repo)


async def get_current_active_user(
    user: UserResponseSchema = Depends(get_current_auth_user),
):
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="inactive user",
    )


async def validate_auth_user(
    login_data: UserLoginRequestSchema,
    repo: UserRepository = Depends(),
) -> UserResponseSchema:
    user = await repo.get_by_username(login_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not verify_password(login_data.password, user.password.encode()):
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
