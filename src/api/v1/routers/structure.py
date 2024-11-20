from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from src.schemas.company import CompanyWithStructure
from src.schemas.structure import CreatePosPayload, StructuresResponse, BasePosition
from src.utils.dependencies import get_service_dep


router = APIRouter(prefix='/structure')


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
):
    # user = await get_current_user_from_token(token)
    pos = await service.add_position(title, company_id, parent_id)
    return BasePosition.model_validate(pos, from_attributes=True)


@router.get(path="/get_position/{pos_id:int}", status_code=HTTP_200_OK)
async def get_position(pos_id, service=get_service_dep("structure")):
    res = await service.get_position(pos_id)
    return BasePosition.model_validate(res, from_attributes=True)

@router.get(path="/{company_id}", status_code=HTTP_200_OK)
async def get_positions(company_id, service=get_service_dep("company")):
    res = await service.get_positions(company_id=company_id)
    return CompanyWithStructure.model_validate(res, from_attributes=True)


@router.get(path="/{position_id:int}/subordinates", status_code=HTTP_200_OK)
async def get_subordinates(position_id, service=get_service_dep("structure")):
    return await service.get_subordinates(pos_id=position_id)


@router.get(path="/{position_id:int}/boss", status_code=HTTP_200_OK)
async def get_boss(position_id, service=get_service_dep("structure")):
    return await service.get_boss(position_id)
