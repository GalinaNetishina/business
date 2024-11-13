"""The module contains base routes for working with company."""

from fastapi import APIRouter

from pydantic import UUID4
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.api.v1.services import TaskService
from src.schemas.task import TaskRequest, CreateTaskResponse, TaskDB, TaskResponse, TaskListResponse

from src.utils.dependencies import token_dep, get_service_dep, get_user_from_token

router = APIRouter(prefix="/task")


@router.post(
    path="/",
    status_code=HTTP_201_CREATED,
)
async def create_task(
    task: TaskRequest,
    user=get_user_from_token,
    service = get_service_dep('task'),
) -> CreateTaskResponse:
    """Create task."""
    created_task = await service.create_task(task)
    return CreateTaskResponse(
        payload=TaskDB.model_validate(created_task, from_attributes=True)
    )


@router.get(
    path='',
    status_code=HTTP_200_OK,
)
async def get_tasks(
    id: UUID4,
    service=get_service_dep('task'),
    # filters
) -> TaskListResponse:
    tasks: TaskDB = await service.get_tasks_by_user_id(id)
    return TaskListResponse(payload=tasks)



