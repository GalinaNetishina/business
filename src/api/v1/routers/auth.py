from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.security import (
    HTTPBearer,
)

from src.api.v1.services.user import UserService
from src.utils import auth as auth_utils

from src.schemas.user import (
    UserRequest,
    UserSchema,
    UserLoginResponse,
    CreateUserResponse,
    UserDB,
    TokenInfo,
    UserResponse,
)

from src.utils.auth_validation import (
    validate_auth_user,
    get_current_user_from_token,
)

http_bearer = HTTPBearer()


router = APIRouter()


@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRequest, service: UserService = Depends(UserService)
):
    created_user = await service.create_user(user_data)
    return CreateUserResponse(
        payload=UserDB.model_validate(created_user, from_attributes=True)
    )


@router.post(
    "/login/", response_model=UserLoginResponse, status_code=status.HTTP_200_OK
)
def auth_user_issue_jwt(user: UserSchema = Depends(validate_auth_user)):
    user = UserSchema.model_validate(user, from_attributes=True)
    token = auth_utils.create_access_token(user)
    payload = TokenInfo(
        access_token=token,
        token_type="Bearer",
    )
    return UserLoginResponse(payload=payload)


@router.get("/users/me/", status_code=status.HTTP_200_OK)
async def auth_user_check_self_info(token=Depends(http_bearer)):
    user = await get_current_user_from_token(token)
    return UserResponse(payload=UserDB.model_validate(user, from_attributes=True))
