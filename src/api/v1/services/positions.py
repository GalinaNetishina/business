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
        await self._check_structure_exists(pos_id)
        res = await self.uow.structure.get_position(pos_id)
        return FullPosition.model_validate(res)

    @transaction_mode
    async def get_root_position(self, company_id):
        return await self.uow.structure.get_root(company_id)

    @transaction_mode
    async def add_position(self, title, company_id, parent_id) -> StructureModel:
        parent = await self.uow.structure.get_position(parent_id)
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
