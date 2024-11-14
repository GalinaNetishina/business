from src.models import TaskModel
from src.utils.repository import SqlAlchemyRepository


class TaskRepository(SqlAlchemyRepository):
    model = TaskModel
