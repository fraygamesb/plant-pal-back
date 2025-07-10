from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from starlette import status

from src.core.utils.security import verify_password
from src.core.repositories.user import UserRepository
from src.core.utils import auth
from src.core.api.v1.schemas.user import UserLoginRequestSchema
from src.core.api.v1.schemas.jwt import TokenInfoSchema

router = APIRouter(prefix="/user", tags=["auth-jwt"])


@router.post("/login", response_model=TokenInfoSchema, status_code=status.HTTP_200_OK)
async def login_user(
    login_data: UserLoginRequestSchema,
    repo: UserRepository = Depends(),
):
    user = await repo.get_by_email(login_data.email)
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
