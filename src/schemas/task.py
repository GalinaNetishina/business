from datetime import datetime

from pydantic import BaseModel, Field, UUID4
from fastapi_filter.contrib.sqlalchemy import Filter
from src.schemas.response import BaseCreateResponse, BaseResponse
from src.schemas.user import UserDB
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
    performer_id: UUID4 | None = None
    observer_id: UUID4 | None = None
    status: Statuses = Statuses.CREATED
    importance: Priorities = Priorities.STANDARD
    tags: list[str] = Field(default_factory=list)


class TaskDB(TaskRequest):
    id: UUID4
    observer: UserDB | None = None
    performer: UserDB | None = None
    start_data: datetime
    update_data: datetime


class TaskFilters(Filter):
    performer_id: UUID4 | None = None
    observer_id: UUID4 | None = None
    status: Statuses = Statuses.CREATED
    importance: Priorities = Priorities.STANDARD
    # tags: list[str] = Field(default_factory=list)


class CreateTaskResponse(BaseCreateResponse):
    payload: TaskDB


class TaskResponse(BaseResponse):
    payload: TaskDB


class TaskListResponse(BaseResponse):
    payload: list[TaskDB]
