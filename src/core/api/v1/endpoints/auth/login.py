from fastapi import (
    APIRouter,
    Depends,
)
from starlette import status

from src.core.utils.validate_auth import validate_auth_user
from src.core.infrastructure.db.models import User
from src.core.utils import auth
from src.core.api.v1.schemas.jwt import TokenInfoSchema

router = APIRouter(prefix="/user", tags=["auth-jwt"])


@router.post("/login", response_model=TokenInfoSchema, status_code=status.HTTP_200_OK)
async def login_user(
    user: User = Depends(validate_auth_user),
):
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "name": user.name,
    }
    token = auth.encode_jwt(payload)
    return TokenInfoSchema(
        access_token=token,
        token_type="Bearer",
    )
