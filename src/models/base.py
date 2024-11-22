from datetime import datetime
from typing import Annotated
from uuid import uuid4

from pydantic import ConfigDict
from sqlalchemy import String, UUID, text, DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column

uuid_pk = Annotated[
    uuid4, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
]
str_uniq = Annotated[str, mapped_column(String, unique=True)]
dt_now_utc_sql = text("TIMEZONE('utc', now())")
created_at = Annotated[datetime, mapped_column(DateTime, server_default=dt_now_utc_sql)]
updated_at = Annotated[
    datetime,
    mapped_column(
        DateTime,
        server_default=dt_now_utc_sql,
        onupdate=dt_now_utc_sql,
    ),
]


class BaseModel(DeclarativeBase):
    __abstract__ = True

    repr_cols_num = 3
    repr_cols = ()

    def __repr__(self) -> str:
        cols = []
        for col, _ in zip(self.__table__.columns.keys(), range(self.repr_cols_num)):
            cols.append(f"{col}={getattr(self, col)}")

        return f'<{self.__class__.__name__} {", ".join(cols)}>'

    model_config = ConfigDict(from_attributes = True)
