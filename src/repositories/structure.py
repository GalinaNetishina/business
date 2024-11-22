from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from src.models import StructureModel
from src.utils.repository import SqlAlchemyRepository


class StructureRepository(SqlAlchemyRepository):
    model = StructureModel

    async def get_position(self, pos_id):
        query = (
            select(self.model)
            .filter_by(id=pos_id)
            .options(joinedload(self.model.boss))
            .options(joinedload(self.model.subordinates))
        )
        res = await self.session.execute(query)
        return res.scalar()

    async def get_subtree(self, pos_id):
        position = await self.get_by_query_one_or_none(id=pos_id)
        if not position:
            return None
        query = select(self.model).filter(self.model.path.descendant_of(position.path))
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
