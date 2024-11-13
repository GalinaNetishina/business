"""The module contains base routes for working with company."""

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from pydantic import UUID4
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.api.v1.services.company import CompanyService
from src.schemas.company import (
    CompanyResponse,
    CompanyWithUsers,
    CompanyRequest,
    CompanyDB,
    CreateCompanyResponse,
    CompanyListResponse,
)
from src.utils.auth_validation import get_current_user_from_token

http_bearer = HTTPBearer()
router = APIRouter(prefix="/company")


@router.post(
    path="/",
    status_code=HTTP_201_CREATED,
)
async def create_company(
    company: CompanyRequest,
    token=Depends(http_bearer),
    service: CompanyService = Depends(CompanyService),
) -> CreateCompanyResponse:
    """Create company."""
    user = await get_current_user_from_token(token)
    created_company = await service.create_company(company, user)
    return CreateCompanyResponse(
        payload=CompanyDB.model_validate(created_company, from_attributes=True)
    )


@router.get(
    path="/{company_id}",
    status_code=HTTP_200_OK,
)
async def get_company_with_users(
    company_id: UUID4,
    service: CompanyService = Depends(CompanyService),
) -> CompanyResponse:
    """Get users by ID company."""
    company: CompanyWithUsers = await service.get_company(company_id)
    return CompanyResponse(payload=company)


@router.get(
    path="",
    status_code=HTTP_200_OK,
)
async def get_companies(
    service: CompanyService = Depends(CompanyService),
) -> CompanyListResponse:
    companies = await service.get_companies()
    return CompanyListResponse(payload=companies)
