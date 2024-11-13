from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from src.models import TaskModel
from src.schemas.task import TaskRequest, TaskDB

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
    async def get_tasks_by_user_id(self, user_id) -> list[TaskDB]:
        res = await self.uow.task.get_by_query_all(id=user_id)
        return list(
            map(lambda x: TaskDB.model_validate(x, from_attributes=True), res)
        )
