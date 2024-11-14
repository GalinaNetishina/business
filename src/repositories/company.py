from sqlalchemy import Result, select
from sqlalchemy.orm import selectinload

from src.models import CompanyModel
from src.utils.repository import SqlAlchemyRepository


class CompanyRepository(SqlAlchemyRepository):
    model = CompanyModel

    async def get_company_with_users(self, company_id) -> CompanyModel | None:
        """Find company by ID with all users."""
        query = (
            select(self.model)
            .where(self.model.id == company_id)
            .options(selectinload(self.model.users))
        )
        res: Result = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def get_companies_with_size(self) -> list[CompanyModel] | None:
        """Find company by ID with all users."""
        query = select(self.model).options(selectinload(self.model.users))
        res: Result = await self.session.execute(query)
        return res.scalars().all()

    # async def get_by_query_short(self, **kwargs: Any) -> CompanyModel:
    #     query = select(self.model).filter_by(**kwargs)
    #     res = await self.session.execute(query)
    #     return res.scalars().all()
