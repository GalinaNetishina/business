from src.models import PositionModel
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class PositionService(BaseService):
    base_repository = "position"

    @transaction_mode
    async def get_subordinates(self, pos_id, **kwargs) -> list[PositionModel]:
        return await self.uow.position.get_subtree(pos_id=pos_id)

    @transaction_mode
    async def get_root_position(self, company_id):
        return await self.uow.position.get_root(company_id)

    @transaction_mode
    async def add_position(self, title, company_id, parent_id) -> PositionModel:
        if parent_id:
            parent = await self.uow.position.get_by_query_one_or_none(id=parent_id)
            pos = PositionModel(name=title, parent=parent)
        else:
            pos = PositionModel(name=title)
        company = await self.uow.company.get_by_query_one_or_none(id=company_id)
        res = await self.uow.position.add_one_and_get_obj(
            **{"name": pos.name, "path": pos.path}
        )
        company.positions.append(res)
        print(company.positions)
        # print(res.boss)
        return res
