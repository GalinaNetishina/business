"""The module contains base routes for working with company."""
from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.api.v1.services.company import CompanyService
from src.schemas.company import (
    CompanyResponse,
    CompanyWithUsers,
    CompanyRequest,
    CompanyDB,
    CreateCompanyResponse,
    CompanyListResponse, CompanyShort, CompanyUpdateRequest,
)
from src.utils.dependencies import token_dep, get_service_dep

router = APIRouter(prefix="/company")


@router.post(
    path="/",
    status_code=HTTP_201_CREATED,
)
async def create_company(
    company: CompanyRequest,
    token=token_dep,
    service = get_service_dep('company'),
) -> CreateCompanyResponse:
    """Create company."""
    # user = await get_current_user_from_token(token)
    # created_company = await service.create_company(company, user)
    created_company = await service.create_company(company)
    return CreateCompanyResponse(
        payload=CompanyDB.model_validate(created_company, from_attributes=True)
    )


@router.get(
    path="/{company_id}",
    status_code=HTTP_200_OK,
)
async def get_company_with_users(
    company_id: UUID4,
    service=get_service_dep('company'),
) -> CompanyResponse:
    company: CompanyWithUsers = await service.get_company_with_users(company_id)
    return CompanyResponse(payload=company)


@router.get(
    path="",
    status_code=HTTP_200_OK,
)
async def get_companies(
    service=get_service_dep('company'),
) -> CompanyListResponse:
    companies = await service.get_companies()
    res = (CompanyShort(**x.model_dump(), size=len(x.users)) for x in companies)
    return CompanyListResponse(payload=list(res))


@router.put(
    path="/{id}",
    status_code=HTTP_200_OK,
)
async def update_company(
    id: UUID4,
    company: CompanyUpdateRequest,
    service=get_service_dep('company'),
) -> CompanyResponse:
    updated_user = await service.update_company(id, company)
    return CompanyResponse(payload=CompanyDB.model_validate(updated_user))


@router.delete(
    "/{id}",
    status_code=HTTP_204_NO_CONTENT,
)
async def delete_company(
    id: UUID4,
    service=get_service_dep('company'),
) -> None:
    await service.delete_company(id)