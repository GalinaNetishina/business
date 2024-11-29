from datetime import datetime

from pydantic import BaseModel, Field, UUID4
from fastapi_filter.contrib.sqlalchemy import Filter
from src.schemas.response import BaseCreateResponse, BaseResponse
from src.utils.enums import Statuses, Priorities


class TaskRequest(BaseModel):
    title: str
    # importance: Priorities = Priorities.STANDARD
    # status: Statuses = Statuses.CREATED

    details: str | None = ""
    tags: list[str] = Field(default_factory=list)

    # additional: dict = Field(default_factory=dict)

    # observer: UserDB | None = None
    # performer: UserDB | None = None


class TaskUpdateRequest(BaseModel):
    id: UUID4
    # performer_id: UUID4 | None = None
    # observer_id: UUID4 | None = None
    status: Statuses = Statuses.CREATED
    importance: Priorities = Priorities.STANDARD
    tags: list[str] = Field(default_factory=list)


class TaskDB(TaskRequest):
    id: UUID4
    start_data: datetime
    update_data: datetime

class TaskFull(TaskDB):
    status: Statuses
    importance: Priorities
    tags: list[str]


class TaskFilters(Filter):
    status: Statuses = Statuses.CREATED
    importance: Priorities = Priorities.STANDARD
    tags: list[str] = Field(default_factory=list)


class CreateTaskResponse(BaseCreateResponse):
    payload: TaskDB


class TaskDetailResponse(BaseResponse):
    payload: TaskFull


class TaskListResponse(BaseResponse):
    payload: list[TaskFull]
