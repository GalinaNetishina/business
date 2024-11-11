from pydantic import BaseModel, Field, UUID4, ConfigDict
from sqlalchemy_utils import Ltree

from src.schemas.response import BaseCreateResponse, BaseResponse
from src.schemas.user import  BaseUser


# from src.schemas.user import UserDB
class BasePosition(BaseModel):
    name: str
    path: Ltree | None  = None
    # parent: UUID4 | None = None
    model_config = ConfigDict (
        arbitrary_types_allowed=True
    )

class Position(BasePosition):
    prev: BasePosition | None = None
    next: BasePosition | None = None


class StructureBase(BaseModel):
    company_id: UUID4
    positions: list[BasePosition]

class CreatePosPayload(BaseModel):
    name: str
    id: UUID4
    parent: str | None = None
    children: list[str] = Field(default_factory=list)


class PositionResponse(BaseCreateResponse):
    payload: CreatePosPayload



