from pydantic import BaseModel, ConfigDict
from starlette.status import HTTP_200_OK, HTTP_201_CREATED


class BaseResponse(BaseModel):
    status: int = HTTP_200_OK
    error: bool = False


class BaseCreateResponse(BaseModel):
    status: int = HTTP_201_CREATED
    error: bool = False


class ErrorResponse(BaseModel):
    error: bool = True
    status: int

    payload: str
    model_config = ConfigDict(arbitrary_types_allowed=True)
