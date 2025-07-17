from fastapi import APIRouter, Depends
from starlette import status

from core.utils.jwt_helper import (
    create_refresh_token,
    create_access_token,
)
from core.api.v1.schemas.user import UserResponseSchema
from core.utils.validate_auth import (
    get_current_active_user,
    get_current_auth_user_for_refresh,
)
from core.utils.validate_auth import validate_auth_user
from core.api.v1.schemas.jwt import TokenInfoSchema


router = APIRouter(prefix="/users", tags=["auth-jwt"])


@router.post(
    "/login",
    response_model=TokenInfoSchema,
    status_code=status.HTTP_200_OK,
)
async def login_user(
    user: UserResponseSchema = Depends(validate_auth_user),
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfoSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    "/refresh",
    response_model=TokenInfoSchema,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
def refresh_jwt(
    user: UserResponseSchema = Depends(get_current_auth_user_for_refresh),
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfoSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get(
    "/me",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def auth_user_check_self_info(
    user: UserResponseSchema = Depends(get_current_active_user),
):
    return UserResponseSchema(
        id=user.id,
        email=user.email,
        name=user.name,
    )
