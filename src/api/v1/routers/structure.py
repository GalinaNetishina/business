from fastapi import APIRouter, Form
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from src.schemas.structure import (
    StructuresResponse,
    BasePosition,
    CreatePosResponse,
    FullPosition,
    PosResponse, UpdatePosition,
)
from src.utils.dependencies import get_service_dep


router = APIRouter(prefix="/structure")


@router.post(
    path="/{company_id}",
    status_code=HTTP_200_OK,
)
async def add_company_positions(
    title: str,
    company_id,
    parent_id: int = None,
    # token=token_dep,
    service=get_service_dep("structure"),
) -> CreatePosResponse:
    # user = await get_current_user_from_token(token)
    pos = await service.add_position(title, company_id, parent_id)
    return CreatePosResponse(payload=BasePosition.model_validate(pos,from_attributes = True))


@router.get(path="/get_position/{pos_id:int}", status_code=HTTP_200_OK)
async def get_position(pos_id, service=get_service_dep("structure"))->PosResponse:
    res = await service.get_position(pos_id)
    return PosResponse(payload=FullPosition.model_validate(res, from_attributes = True))

@router.patch(path='/{pos_id:int}', status_code=HTTP_200_OK)
async def update_position(
        pos_id,
        data: UpdatePosition = Form(...),
        service=get_service_dep("structure")
)->PosResponse:
    updated = await service.update_position(pos_id, data)
    return PosResponse(payload=updated)


@router.delete(path="/{pos_id:int}", status_code=HTTP_204_NO_CONTENT)
async def delete_position(pos_id, service=get_service_dep("structure")) -> None:
    await service.delete_position(pos_id)
