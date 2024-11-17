from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from src.models import TaskModel
from src.schemas.task import TaskRequest, TaskDB, TaskUpdateRequest

from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class TaskService(BaseService):
    base_repository: str = "task"

    @transaction_mode
    async def create_task(self, task: TaskRequest) -> TaskModel:
        return await self.uow.task.add_one_and_get_obj(
            **task.model_dump(),
        )

    @transaction_mode
    async def update_task(self, task: TaskUpdateRequest):
        await self._check_task_exists(task.id)
        res = await self.uow.task.update_one_by_id(
            task.id, **task.model_dump(exclude_unset=True)
        )
        return TaskDB.model_validate(res, from_attributes=True)

    @transaction_mode
    async def delete_task(self, id) -> None:
        await self._check_task_exists(id)
        await self.uow.task.delete_by_query(id=id)

    @transaction_mode
    async def get_tasks_by_query(self, **kwargs) -> list[TaskDB]:
        res = await self.uow.task.get_by_query_all(**kwargs)
        return list(map(lambda x: TaskDB.model_validate(x, from_attributes=True), res))

    async def _check_task_exists(self, id) -> None:
        exist = await self.uow.task.check_exists(id)
        if not exist:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Task not found")
