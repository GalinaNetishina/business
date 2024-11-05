from pydantic import  BaseModel, Field, EmailStr


from src.schemas.response import BaseCreateResponse, BaseResponse


class UserRequest(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str | None = None
    company_id: int | None = None
    is_active: bool = True


class UserLoginRequest(UserRequest):
    # first_name: str = Field(max_length=50)
    # last_name: str = Field(max_length=50)
    # email: str | None = Field(EmailStr, max_length=70)
    # is_active: bool = True
    password: bytes

class UserUpdateRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    company_id: int | None = None

class UserDB(UserRequest):
    id: int


class CreateUserResponse(BaseCreateResponse):
    payload: UserDB


class UserResponse(BaseResponse):
    payload: UserDB


class UsersListResponse(BaseResponse):
    payload: list[UserDB]


