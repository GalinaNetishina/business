from sqlalchemy import select, func

from src.models import StructureModel
from src.utils.repository import SqlAlchemyRepository


class StructureRepository(SqlAlchemyRepository):
    model = StructureModel

    async def get_subtree(self, pos_id):
        position = await self.get_by_query_one_or_none(id=pos_id)
        if not position:
            return None
        query = select(self.model).filter(self.model.path.descendant_of(position.path))
        res = await self.session.execute(query)
        return res.scalars().all()[1:]

    async def get_boss(self, pos_id):
        position = await self.get_by_query_one_or_none(id=pos_id)
        if not position:
            return None
        query = select(self.model).filter(self.model.path.ancestor_of(position.path))
        res = await self.session.execute(query)
        return res.scalars().all()[-2:-1]

    async def get_root(self, company_id):
        query = (
            select(self.model)
            .where(self.model.company_id == company_id)
            .filter(func.nlevel(self.model.path) == 1)
        )
        res = await self.session.execute(query)
        return res.scalars().all()
