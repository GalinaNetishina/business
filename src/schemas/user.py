from pydantic import  BaseModel, Field, EmailStr, field_validator, model_validator

from src.schemas.response import BaseCreateResponse, BaseResponse


class BaseUser(BaseModel):
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)

class UserRequest(BaseUser):
    email: str | None = None
    password: str | bytes
    company_id: int | None = None
    is_active: bool = True

class UserSchema(BaseUser):
    password: str | bytes
    email: EmailStr | None = None
    active: bool = True

class UserUpdateRequest(BaseUser):
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


