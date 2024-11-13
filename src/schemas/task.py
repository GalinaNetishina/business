from datetime import datetime

from pydantic import BaseModel, Field, UUID4

from src.schemas.response import BaseCreateResponse, BaseResponse
from src.schemas.user import UserDB
from src.utils.enums import Priorities, Statuses


class TaskRequest(BaseModel):
    title: str
    # importance: Priorities = Priorities.STANDARD
    # status: Statuses = Statuses.CREATED

    details: str | None
    tags: list[str]  = Field(default_factory=list)

    # additional: dict = Field(default_factory=dict)

    # observer: UserDB | None = None
    # performer: UserDB | None = None


class TaskDB(TaskRequest):
    id: UUID4
    start_data: datetime
    update_data: datetime


class CreateTaskResponse(BaseCreateResponse):
    payload: TaskDB


class TaskResponse(BaseResponse):
    payload: TaskDB


class TaskListResponse(BaseResponse):
    payload: list[TaskDB]
