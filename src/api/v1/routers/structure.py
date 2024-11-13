from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from starlette.status import HTTP_200_OK


from src.schemas.structure import PositionResponse
from src.utils.dependencies import get_service_dep, token_dep

http_bearer = HTTPBearer()
# @router.post(
#     path="/",
#     status_code=HTTP_201_CREATED,
# )
# async def create_position(
#     position: str,
#     boss = None,
#     service  = Depends(PositionService),
# ):
#     created_position = await service.create_position(position)
#     return {created_position}
#
router1 = APIRouter(prefix="/position")


@router1.post(
    path="/{company_id}",
    status_code=HTTP_200_OK,
)
async def add_company_positions(
    title: str,
    company_id,
    parent_id=None,
    # token=token_dep,
    service=get_service_dep('structure'),
):
    # user = await get_current_user_from_token(token)

    pos = await service.add_position(title, company_id, parent_id)
    payload = {"name": pos.name, "id": pos.id}
    return PositionResponse(payload=payload)
