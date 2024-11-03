from pydantic import  BaseModel, Field, EmailStr

from src.schemas.response import BaseCreateResponse, BaseResponse


class UserRequest(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str | None = Field(EmailStr, max_length=70)
    company_id: int

class UserUpdateRequest(BaseModel):
    first_name: str | None = Field(max_length=50)
    last_name: str | None = Field(max_length=50)
    email: str | None = Field(EmailStr, max_length=70)
    company_id: int | None

class UserDB(UserRequest):
    id: int


class CreateUserResponse(BaseCreateResponse):
    payload: UserDB


class UserResponse(BaseResponse):
    payload: UserDB


class UsersListResponse(BaseResponse):
    payload: list[UserDB]


