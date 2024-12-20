from pydantic import BaseModel, Field, UUID4, field_validator

from src.schemas.response import BaseCreateResponse, BaseResponse
from src.schemas.structure import BasePosition
from src.schemas.user import UserDB


class CompanyRequest(BaseModel):
    inn: int
    company_name: str = Field(max_length=50)


class CompanyUpdateRequest(BaseModel):
    inn: int | None = None
    company_name: str | None = None


class CompanyDB(CompanyRequest):
    id: UUID4


class CompanyUpdateResponse(BaseResponse):
    payload: CompanyDB


class CompanyWithUsers(CompanyDB):
    users: list[UserDB] | None = Field(default_factory=list)


class CompanyWithStructure(CompanyDB):
    structure: list[BasePosition] = Field(default_factory=list)

    @field_validator('structure')
    @classmethod
    def structure_ordering(cls, value):
        return sorted(value, key = lambda x: (len(x.path), x.path))


class CompanyShort(CompanyDB):
    size: int


class CreateCompanyResponse(BaseCreateResponse):
    payload: CompanyDB


class CompanyResponse(BaseResponse):
    payload: CompanyWithUsers


class CompanyListResponse(BaseResponse):
    payload: list[CompanyShort]
