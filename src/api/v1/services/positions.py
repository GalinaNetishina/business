from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from src.models import PositionModel
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class PositionService(BaseService):
    base_repository = "position"

    @transaction_mode
    async def get_subordinates(self, pos_id, **kwargs) -> list[PositionModel]:
        await self._check_structure_exists(id=pos_id)
        return await self.uow.position.get_subtree(pos_id=pos_id)

    @transaction_mode
    async def get_boss(self, pos_id, **kwargs) -> list[PositionModel]:
        await self._check_structure_exists(id=pos_id)
        return await self.uow.position.get_boss(pos_id=pos_id)


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
        res = await self.uow.position.add_one_and_get_obj(
            name=pos.name, path= pos.path, company_id= company_id)
        return res

    async def _check_structure_exists(self, id) -> None:
        exist = await self.uow.position.check_exists(id)
        if not exist:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="Structure not found"
            )
