from fastapi import APIRouter, Depends
from starlette import status

from src.core.api.v1.schemas.user import UserResponseSchema
from src.core.utils.validate_auth import get_current_auth_user
from src.core.utils.validate_auth import validate_auth_user
from src.core.utils import auth
from src.core.api.v1.schemas.jwt import TokenInfoSchema


router = APIRouter(prefix="/user", tags=["auth-jwt"])


@router.post("/login", response_model=TokenInfoSchema, status_code=status.HTTP_200_OK)
async def login_user(
    user: UserResponseSchema = Depends(validate_auth_user),
):
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "name": user.name,
    }
    token = auth.encode_jwt(payload)
    return TokenInfoSchema(
        access_token=token,
    )


@router.get("/me", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
async def auth_user_check_self_info(
    user: UserResponseSchema = Depends(get_current_auth_user),
):
    return UserResponseSchema(
        id=user.id,
        email=user.email,
        name=user.name,
    )
