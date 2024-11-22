from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
    UUID4,
    ConfigDict,
    PlainValidator,
    PlainSerializer,
    WithJsonSchema,
)
from sqlalchemy_utils import Ltree

from src.schemas.response import BaseCreateResponse, BaseResponse

LTreeField = Annotated[
    Ltree,
    PlainValidator(lambda v: Ltree(v)),
    PlainSerializer(lambda v: v.path),
    WithJsonSchema({"type": "string", "examples": ["same.path"]}),
]

class BasePosition(BaseModel):
    id: int
    name: str
    path: LTreeField | None = None
    model_config = ConfigDict(arbitrary_types_allowed=True)


class FullPosition(BasePosition):
    boss: BasePosition | None
    subordinates: list[BasePosition] = Field(default_factory=list)

class UpdatePosition(BaseModel):
    name: str | None = None
    boss: BasePosition | None = None
    subordinates: list[BasePosition] = Field(default_factory=list)


class StructureBase(BaseModel):
    company_id: UUID4
    positions: list[FullPosition]


class CreatePosResponse(BaseCreateResponse):
    payload: BasePosition


class PosResponse(BaseResponse):
    payload: FullPosition


class StructuresResponse(BaseResponse):
    payload: list[BasePosition]
