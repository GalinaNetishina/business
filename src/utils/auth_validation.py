from fastapi import Depends, HTTPException, Form
from fastapi.security import HTTPBearer
from jwt import InvalidTokenError
from starlette import status

from src.api.v1.services.user import UserService
from src.utils.auth import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    decode_jwt, encode_jwt, verify_password
)

from src.schemas.user import UserSchema, UserRequest, UserDB
http_bearer = HTTPBearer()
# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="/api/v1/demo-auth/jwt/login/",)
# )


def get_current_token_payload(
    token: str = Depends(http_bearer),
) -> dict:
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
    )


async def get_user_by_token_sub(payload: dict,
                          service: UserService = Depends(UserService)) -> UserRequest:
    email: str | None = payload.get("sub")
    user = await service.get_user_by_email(email)
    if user:
        return UserRequest(payload=UserDB.model_validate(user, from_attributes=True))
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


async def get_auth_user_from_token_of_type(token_type: str):
    async def get_auth_user_from_token(
        payload: dict = Depends(get_current_token_payload),
    ) ->UserSchema:
        validate_token_type(payload, token_type)
        res = await get_user_by_token_sub(payload)
        return res
    res = await get_auth_user_from_token
    return res


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(
        self,
        payload: dict = Depends(get_current_token_payload),
    ):
        validate_token_type(payload, self.token_type)
        return get_user_by_token_sub(payload)


# get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)

get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


async def get_current_active_auth_user(
    # user: UserSchema = Depends(get_current_auth_user),
):
    user = await get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)

    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="inactive user",
    )


async def validate_auth_user(
    email: str = Form(),
    password: str = Form(),
):
    service = UserService()
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    user = await service.get_user_by_email(email)
    if not user:
        raise unauthed_exc

    if not verify_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauthed_exc

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user