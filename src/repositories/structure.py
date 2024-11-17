from sqlalchemy import select, func

from src.models import PositionModel, StructureModel
from src.utils.repository import SqlAlchemyRepository


class StructureRepository(SqlAlchemyRepository):
    model = StructureModel


class PositionRepository(SqlAlchemyRepository):
    model = PositionModel

    async def get_subtree(self, pos_id):
        position = await self.get_by_query_one_or_none(id=pos_id)
        query = select(self.model).filter(self.model.path.descendant_of(position.path))
        print(query)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_root(self, company_id):
        query = (
            select(self.model)
            .where(self.model.company_id == company_id)
            .filter(func.nlevel(self.model.path) == 1)
        )
        res = await self.session.execute(query)
        return res.scalars().all()
