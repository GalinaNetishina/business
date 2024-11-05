from jwt.exceptions import InvalidTokenError
from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from pydantic import BaseModel

from src.api.v1.services.user import UserService
from src.utils import auth as auth_utils

from src.schemas.user import UserRequest, UserSchema, CreateUserResponse, UserDB
from src.utils.auth_validation import validate_auth_user, get_current_token_payload, get_current_active_auth_user

http_bearer = HTTPBearer()


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
)


@router.post("/register/")
async def register_user(
        user_data: UserRequest,
        service: UserService = Depends(UserService)
):
    user = await service.get_user_by_email(user_data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='user exists')

    created_user = await service.create_user(user_data)
    return CreateUserResponse(payload=UserDB.model_validate(created_user, from_attributes=True))



@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserSchema= Depends(validate_auth_user)
):
    token = auth_utils.create_access_token(user)
    # refresh_token = auth_utils.create_refresh_token(user)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@router.get("/users/me/")
async def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema= Depends(get_current_active_auth_user)
):

    iat = payload.get("iat")

    return {
        **user,
        "logged_in_at": iat,
    }