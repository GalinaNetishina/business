"""The module contains base routes for working with company."""

from fastapi import APIRouter, Form, Depends

from pydantic import UUID4
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.schemas.task import (
    TaskRequest,
    CreateTaskResponse,
    TaskDB,
    TaskListResponse,
    TaskUpdateRequest,
    TaskFilters,
)

from src.utils.dependencies import get_service_dep, get_user_from_token

router = APIRouter(prefix="/task")


@router.post(
    path="/",
    status_code=HTTP_201_CREATED,
)
async def create_task(
    task: TaskRequest,
    user=get_user_from_token,
    service=get_service_dep("task"),
) -> CreateTaskResponse:
    """Create task."""
    created_task = await service.create_task(task)
    return CreateTaskResponse(
        payload=TaskDB.model_validate(created_task, from_attributes=True)
    )


@router.get(
    path="",
    status_code=HTTP_200_OK,
)
async def get_tasks_with_filters(
    service=get_service_dep("task"), filters: TaskFilters = Depends(TaskFilters)
) -> TaskListResponse:
    tasks: list[TaskDB] = await service.get_tasks_by_query(
        **filters.model_dump(exclude_unset=True)
    )
    return TaskListResponse(payload=tasks)


@router.patch(path="/{id}", status_code=HTTP_200_OK)
async def update_task_status(
    task: TaskUpdateRequest = Form(...), service=get_service_dep("task")
):
    task = await service.update_task(task)
    return task


@router.delete(
    "/{id}",
    status_code=HTTP_204_NO_CONTENT,
)
async def delete_task(
    id: UUID4,
    service=get_service_dep("task"),
):
    await service.delete_task(id)
