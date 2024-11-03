from pydantic import BaseModel, Field

from src.schemas.response import BaseCreateResponse, BaseResponse
from src.schemas.user import UserDB

class CompanyRequest(BaseModel):
    inn: int
    company_name: str = Field(max_length=50)


class CompanyDB(CompanyRequest):
    id: int


class CompanyWithUsers(CompanyDB):
    users: list[UserDB] = Field(default_factory=list)


class CreateCompanyResponse(BaseCreateResponse):
    payload: CompanyDB


class CompanyResponse(BaseResponse):
    payload: CompanyWithUsers


class CompanyListResponse(BaseResponse):
    payload: list[CompanyRequest]
