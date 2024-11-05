from jwt.exceptions import InvalidTokenError
from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPBearer, HTTPAuthorizationCredentials,
    # HTTPAuthorizationCredentials,
    # OAuth2PasswordBearer,
)
from pydantic import BaseModel

from src.api.auth import utils as auth_utils
from src.schemas.user import UserRequest, UserLoginRequest

http_bearer = HTTPBearer()
# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="/api/v1/demo-auth/jwt/login/",
# )


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(prefix="/jwt", tags=["JWT"])

john = UserLoginRequest(
    first_name="john",
    last_name="dow",
    password=auth_utils.hash_password("qwerty"),
    email="john@example.com",
)
sam = UserLoginRequest(
    first_name="sam",
    last_name="smith",
    password=auth_utils.hash_password("secret"),
)

users_db: dict[str, UserLoginRequest] = {
    'john': john,
    'sam': sam,
}


def validate_auth_user(
    first_name: str = Form(),
    last_name: str = Form(),
    password: str = Form(),
):
    unauthorized_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    if not (user := users_db.get(first_name)):
        raise unauthorized_exc

    if not auth_utils.validate_password(
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


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> dict:
    token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(
            token=token
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
            # detail=f"invalid token error",
        )
    return payload


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserRequest:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def get_current_active_auth_user(
    user: UserRequest= Depends(get_current_auth_user),
):
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserRequest = Depends(validate_auth_user),
):
    jwt_payload = {
        # subject
        "sub": user.first_name,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        # "logged_in_at"
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@router.get("/users/me/")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserRequest = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "logged_in_at": iat,
    }