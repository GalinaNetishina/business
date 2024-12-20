from sqlalchemy import select, func, update
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import expression
from sqlalchemy_utils.types.ltree import LQUERY

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

    async def get_by_path_part(self, id):
        template = f"*.{id}.*"
        query = select(self.model).filter(
            self.model.path.lquery(expression.cast(template, LQUERY))
        )
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_by_path_part_any(self, template):
        query = select(self.model).filter(
            self.model.path.lquery(expression.cast(template, LQUERY))
        )
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

    async def update_one_by_id(self, obj_id, **kwargs):
        query = (
            update(self.model)
            .filter(self.model.id == obj_id)
            .values(**kwargs)
            .returning(self.model)
        )
        obj = await self.session.execute(query)
        return obj.scalar_one_or_none()
