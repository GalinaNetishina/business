"""The module contains base classes for working with databases."""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from sqlalchemy import exists
from typing import Any, TypeVar
from typing_extensions import Never

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import BaseModel


class AbstractRepository(ABC):
    """An abstract class implementing the CRUD operations for working with any database."""

    @abstractmethod
    async def add_one(self, *args: Any, **kwargs: Any) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def add_one_and_get_id(self, *args: Any, **kwargs: Any) -> Never:
        raise NotImplementedError

    async def add_one_and_get_obj(self, *args: Any, **kwargs: Any) -> Never:
        raise NotImplementedError

    async def get_by_query_one_or_none(self, *args: Any, **kwargs: Any) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def get_by_query_all(self, *args: Any, **kwargs: Any) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def update_one_by_id(self, *args: Any, **kwargs: Any) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_query(self, *args: Any, **kwargs: Any) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def delete_all(self, *args: Any, **kwargs: Any) -> Never:
        raise NotImplementedError


M = TypeVar("M", bound=BaseModel)


class SqlAlchemyRepository(AbstractRepository):
    """A basic repository that implements basic CRUD functions with a base table using the SqlAlchemy library.

    params:
        - model: SQLAlchemy child DeclarativeBase class
    """

    model: M

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one(self, **kwargs: Any) -> None:
        query = insert(self.model).values(**kwargs)
        await self.session.execute(query)

    async def check_exists(self, id):
        query = select(exists(self.model).where(self.model.id == id))
        res = await self.session.execute(query)
        return res.scalar()

    async def add_one_and_get_id(self, **kwargs: Any) -> int | str:
        query = insert(self.model).values(**kwargs).returning(self.model.id)
        obj_id = await self.session.execute(query)
        return obj_id.scalar_one()

    async def add_one_and_get_obj(self, **kwargs: Any) -> M:
        query = insert(self.model).values(**kwargs).returning(self.model)
        obj = await self.session.execute(query)
        return obj.scalar_one()

    async def get_by_query_one_or_none(self, **kwargs: Any) -> M | None:
        query = select(self.model).filter_by(**kwargs)
        res = await self.session.execute(query)
        return res.unique().scalar_one_or_none()

    async def get_by_query_all(self, **kwargs: Any) -> Sequence[M]:
        query = select(self.model).filter_by(**kwargs)
        # print(query, kwargs)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def update_one_by_id(self, obj_id: int | str, **kwargs: Any) -> M | None:
        query = (
            update(self.model)
            .filter(self.model.id == obj_id)
            .values(**kwargs)
            .returning(self.model)
        )
        obj = await self.session.execute(query)
        return obj.scalar_one_or_none()

    async def delete_by_query(self, **kwargs: Any) -> None:
        query = delete(self.model).filter_by(**kwargs)
        await self.session.execute(query)

    async def delete_all(self) -> None:
        query = delete(self.model)
        await self.session.execute(query)
