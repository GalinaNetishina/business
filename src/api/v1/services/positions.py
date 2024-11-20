
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from src.models import StructureModel
from src.schemas.structure import BasePosition, FullPosition
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class StructureService(BaseService):
    base_repository = "structure"

    @transaction_mode
    async def get_position(self, pos_id) -> BasePosition | None:
        res= await self.uow.structure.get_by_query_one_or_none(id=pos_id)
        res.boss = await self.get_boss(res.id)
        res.subordinates = await self.get_subordinates(res.id)
        return FullPosition.model_validate(res)

    @transaction_mode
    async def get_subordinates(self, pos_id, **kwargs) -> list[StructureModel]:
        await self._check_structure_exists(id=pos_id)
        return await self.uow.structure.get_subtree(pos_id=pos_id)

    @transaction_mode
    async def get_boss(self, pos_id, **kwargs) -> list[StructureModel]:
        await self._check_structure_exists(id=pos_id)
        return await self.uow.structure.get_boss(pos_id=pos_id)

    @transaction_mode
    async def get_root_position(self, company_id):
        return await self.uow.structure.get_root(company_id)

    @transaction_mode
    async def add_position(self, title, company_id, parent_id) -> StructureModel:

        parent = await self.uow.structure.get_by_query_one_or_none(id=parent_id)
        res = await self.uow.structure.add_one_and_get_obj(
            **StructureModel(name=title, parent=parent).to_dict(),
            # company_id=company_id
        )
        await self.uow.structure.update_one_by_id(res.id, company_id=company_id)
        return res

    async def _check_structure_exists(self, id) -> None:
        exist = await self.uow.structure.check_exists(id)
        if not exist:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="Structure not found"
            )
