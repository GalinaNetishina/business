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


# from src.schemas.user import UserDB
class BasePosition(BaseModel):
    id: int
    name: str
    path: LTreeField | None = None
    # parent: UUID4 | None = None
    model_config = ConfigDict(arbitrary_types_allowed=True)


class FullStructure(BasePosition):
    boss: BasePosition | None = None
    subordinates: list[BasePosition] = Field(default_factory=list)
    model_config = ConfigDict(arbitrary_types_allowed=True)


class StructureBase(BaseModel):
    company_id: UUID4
    positions: list[FullStructure]
    model_config = ConfigDict(arbitrary_types_allowed=True)


class CreatePosPayload(BaseCreateResponse):
    payload: FullStructure
    model_config = ConfigDict(arbitrary_types_allowed=True)

class StructuresResponse(BaseResponse):
    payload: list[BasePosition]
