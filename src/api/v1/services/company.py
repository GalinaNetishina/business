from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from src.models import CompanyModel
from src.schemas.company import CompanyWithUsers, CompanyRequest, CompanyUpdateRequest
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class CompanyService(BaseService):
    base_repository: str = "company"

    @transaction_mode
    # async def create_company(self, company: CompanyRequest, admin) -> CompanyModel:
    async def create_company(self, company: CompanyRequest) -> CompanyModel:
        """Create company."""
        return await self.uow.company.add_one_and_get_obj(
            **company.model_dump(),
            # admin_id=admin.id
        )

    @transaction_mode
    async def get_companies(self) -> list[CompanyWithUsers]:
        res = await self.uow.company.get_companies_with_size()
        return list(
            map(lambda x: CompanyWithUsers.model_validate(x, from_attributes=True), res)
        )

    @transaction_mode
    async def get_company_with_users(self, company_id) -> CompanyWithUsers:
        await self._check_company_exists(id)
        company: CompanyModel | None = await self.uow.company.get_company_with_users(
            company_id
        )
        return CompanyWithUsers.model_validate(company, from_attributes=True)

    @transaction_mode
    async def get_company_positions(self, company_id) -> CompanyWithUsers:
        await self._check_company_exists(id)
        company: CompanyModel | None = await self.uow.company.get_company_positions(
            company_id
        )
        return CompanyWithUsers.model_validate(company, from_attributes=True)

    @transaction_mode
    async def update_user(self, id, company: CompanyUpdateRequest) -> CompanyModel:
        await self._check_company_exists(id)
        company: CompanyModel | None = await self.uow.company.update_one_by_id(
            obj_id=id, **company.model_dump(exclude_unset=True)
        )
        return company

    @transaction_mode
    async def delete_company(self, id) -> None:
        # company: CompanyModel | None = await self.uow.company.get_company_with_users(id)
        await self._check_company_exists(id)
        await self.uow.company.delete_by_query(id=id)

    async def _check_company_exists(self, id) -> None:
        exist = await self.uow.company.check_exists(id)
        if not exist:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="Company not found"
            )
