"""The module contains base routes for working with company."""

from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.api.v1.services.company import CompanyService
from src.schemas.company import CompanyResponse, CompanyWithUsers, CompanyRequest, CompanyDB, CreateCompanyResponse
from src.schemas.user import UserRequest

router = APIRouter(prefix='/company')


@router.post(
    path='/',
    status_code=HTTP_201_CREATED,
)
async def create_company(
        company: CompanyRequest,
        service: CompanyService = Depends(CompanyService),
) -> CreateCompanyResponse:
    """Create company."""
    created_company= await service.create_company(company)
    return CreateCompanyResponse(payload=CompanyDB.model_validate(created_company, from_attributes=True))


@router.get(
    path='/{company_id}',
    status_code=HTTP_200_OK,
)
async def get_company_with_users(
        company_id: int,
        service: CompanyService = Depends(CompanyService),
) -> CompanyResponse:
    """Get users by ID company."""
    company: CompanyWithUsers = await service.get_company_with_users(company_id)
    return CompanyResponse(payload=company)
