import json

from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from confluent_kafka import Producer
from src.task_service.task_schemas import TaskRequest, TaskDB, TaskUpdateRequest, TaskFull

from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode
conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)


def delivery_new_status(err, msg):
    if err is not None:
        print(f'error in sending message:{err}')
    else:
        print(f'message {msg} sended in {msg.topic()} [{msg.partition()}]')

class TaskService(BaseService):
    base_repository: str = "task"

    @transaction_mode
    async def create_task(self, task: TaskRequest) -> TaskDB:
        res = await self.uow.task.add_one_and_get_obj(
            **task.model_dump(),
        )
        return TaskDB.model_validate(res, from_attributes=True)

    @transaction_mode
    async def update_task_status(self, task: TaskUpdateRequest) :
        await self._check_task_exists(task.id)
        topic='status'
        producer.produce(topic, key=f'task_{task.id}', value=task.model_dump_json(), callback=delivery_new_status)
        producer.flush()


    @transaction_mode
    async def delete_task(self, id) -> None:
        await self._check_task_exists(id)
        await self.uow.task.delete_by_query(id=id)

    @transaction_mode
    async def get_tasks_by_query(self, **kwargs) -> list[TaskDB]:
        res = await self.uow.task.get_by_query_all(**kwargs)
        return list(map(lambda x: TaskFull.model_validate(x, from_attributes=True), res))

    @transaction_mode
    async def get_task_by_id(self, id) -> TaskFull:
        await self._check_task_exists(id)
        res = await self.uow.task.get_by_query_one_or_none(id=id)
        return TaskFull.model_validate(res, from_attributes=True)

    async def _check_task_exists(self, id) -> None:
        exist = await self.uow.task.check_exists(id)
        if not exist:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Task not found")
