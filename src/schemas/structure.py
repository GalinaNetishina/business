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

from src.schemas.response import BaseCreateResponse

LTreeField = Annotated[
    Ltree,
    PlainValidator(lambda v: Ltree(v)),
    PlainSerializer(lambda v: v.path),
    WithJsonSchema({"type": "string", "examples": ["same.path"]}),
]


# from src.schemas.user import UserDB
class BasePosition(BaseModel):
    name: str
    path: LTreeField | None = None
    # parent: UUID4 | None = None
    model_config = ConfigDict(arbitrary_types_allowed=True)


class FullPosition(BasePosition):
    boss: BasePosition | None = None
    subordinates: list[BasePosition] = Field(default_factory=list)
    model_config = ConfigDict(arbitrary_types_allowed=True)


# class Position(BasePosition):
#     prev: BasePosition | None = None
#     next: BasePosition | None = None


class StructureBase(BaseModel):
    company_id: UUID4
    positions: list[BasePosition]
    model_config = ConfigDict(arbitrary_types_allowed=True)


class CreatePosPayload(BaseCreateResponse):
    payload: FullPosition
    model_config = ConfigDict(arbitrary_types_allowed=True)
