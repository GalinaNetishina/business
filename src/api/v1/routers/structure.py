from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from src.schemas.structure import PositionResponse, CreatePosPayload
from src.utils.dependencies import get_service_dep


router = APIRouter()


@router.post(
    path="/{company_id}",
    status_code=HTTP_200_OK,
)
async def add_company_positions(
    title: str,
    company_id,
    parent_id: int = None,
    # token=token_dep,
    service=get_service_dep("position"),
):
    # user = await get_current_user_from_token(token)
    pos = await service.add_position(title, company_id, parent_id)
    return PositionResponse(
        payload=CreatePosPayload.model_validate(pos, from_attributes=True)
    )


# TODO  почему-то вызывается вместо task.get_with_filters
# @router.get(path='/{company_id}', status_code=HTTP_200_OK)
# async def get_positions(company_id, service=get_service_dep("company")):
# return await service.get_positions(company_id=company_id)

# TODO баг - возвращает саму позицию с подчиненными, и путь странный
@router.get(path="/{position_id:int}/subordinates", status_code=HTTP_200_OK)
async def get_subordinates(position_id, service=get_service_dep("position")):
    return await service.get_subordinates(pos_id=position_id)
