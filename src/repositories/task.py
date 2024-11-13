from sqlalchemy import Result, select
from sqlalchemy.orm import selectinload

from src.models import TaskModel
from src.schemas.task import TaskRequest
from src.utils.repository import SqlAlchemyRepository


class TaskRepository(SqlAlchemyRepository):
    model = TaskModel

