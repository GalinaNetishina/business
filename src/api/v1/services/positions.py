from src.models import PositionModel
from src.schemas.structure import BasePosition
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class PositionService(BaseService):
    base_repository = "position"

    @transaction_mode
    async def add_position(self, title, company_id, parent_id) -> PositionModel:
        if parent_id:
            parent = await self.get_by_query_one_or_none(id=parent_id)
        else:
            parent = None
        pos = PositionModel(name=title, parent=parent)
        pos_dto = BasePosition(name=title, path=pos.path)
        print(pos, "\n", pos_dto)
        res = await self.uow.structure.add_one_and_get_obj(**pos_dto.model_dump())
        print(res)
        return res
