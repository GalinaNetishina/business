from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from src.models import CompanyModel, PositionModel
from src.schemas.company import CompanyWithUsers, CompanyRequest, CompanyDB
from src.schemas.structure import BasePosition
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class CompanyService(BaseService):
    base_repository: str = "company"

    @transaction_mode
    async def create_company(self, company: CompanyRequest, admin) -> CompanyModel:
        """Create company."""
        return await self.uow.company.add_one_and_get_obj(
            **company.model_dump(), admin_id=admin.id
        )

    @transaction_mode
    async def get_companies(self) -> list[CompanyDB]:
        res = await self.uow.company.get_by_query_all()
        return list(
            map(lambda x: CompanyDB.model_validate(x, from_attributes=True), res)
        )

    @transaction_mode
    async def get_company(self, company_id) -> CompanyWithUsers:
        """Find company by ID with all users."""
        company: CompanyModel | None = await self.uow.company.get_company(company_id)
        self._check_company_exists(company)
        return CompanyWithUsers.model_validate(company, from_attributes=True)

    @transaction_mode
    async def get_company_positions(self, company_id) -> CompanyWithUsers:
        company: CompanyModel | None = await self.uow.company.get_company_positions(
            company_id
        )
        self._check_company_exists(company)
        return CompanyWithUsers.model_validate(company, from_attributes=True)

    @staticmethod
    def _check_company_exists(company: CompanyModel | None) -> None:
        if not company:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="Company not found"
            )


class PositionService(BaseService):
    base_repository = "position"

    @transaction_mode
    async def add_position(self, title, company_id, parent_id) -> PositionModel:
        if parent_id:
            parent = await self.get_by_query_one_or_none(id=parent_id)
        else:
            parent = None
        pos = PositionModel(name=title, parent=parent)
        pos_dto = BasePosition(name=title, path=pos.path)
        print(pos, "\n", pos_dto)
        res = await self.uow.structure.add_one_and_get_obj(**pos_dto.model_dump())
        print(res)
        return res
