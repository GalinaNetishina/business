from fastapi import HTTPException, Form
from fastapi.security import HTTPBearer
from jwt import InvalidTokenError
from starlette import status

from src.api.v1.services.user import UserService
from src.models import UserModel
from src.utils.auth import decode_jwt, verify_password

http_bearer = HTTPBearer()


def get_current_token_payload(token) -> dict:
    try:
        payload = decode_jwt(
            token=token.credentials,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


async def get_user_by_token_sub(
    payload: dict,
) -> UserModel:
    service = UserService()
    email: str | None = payload.get("sub")
    user = await service.get_user_by_email(email)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def get_current_user_from_token(token):
    payload = get_current_token_payload(token)
    return get_user_by_token_sub(payload)


async def validate_auth_user(
    email: str = Form(),
    password: str = Form(),
):
    service = UserService()
    unauthorized_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email or password",
    )
    user = await service.get_user_by_email(email)
    if not user:
        raise unauthorized_exc

    if not verify_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauthorized_exc

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )
    return user
