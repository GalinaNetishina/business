from sqlalchemy import Result, select

from src.models import CompanyModel, PositionModel
from src.utils.repository import SqlAlchemyRepository


class StructureRepository(SqlAlchemyRepository):
    model = PositionModel

    async def get_positions(self) -> CompanyModel | None:
        query = (
            select(self.model)
            # .where(self.model.company_id == company_id)
        )
        res: Result = await self.session.execute(query)
        return res.scalar_one_or_none()

    # async def get_company_positions(self, company_id) -> CompanyModel | None:
    #     """Find company by ID with all positions."""
    #     query = (
    #         select(self.submodel)
    #         .where(self.submodel.company_id == company_id)
    #     )
    #     res: Result = await self.session.execute(query)
    #     return res.scalar_one_or_none()
