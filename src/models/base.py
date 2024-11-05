from typing import Annotated

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, mapped_column

int_pk = Annotated[int, mapped_column(Integer, primary_key=True)]
str_uniq = Annotated[str, mapped_column(String, unique=True)]

class BaseModel(DeclarativeBase):
    __abstract__ = True

    repr_cols_num = 3
    repr_cols = ()

    def __repr__(self) -> str:
        cols = []
        for col, _ in zip(self.__table__.columns.keys(), range(self.repr_cols_num)):
            cols.append(f'{col}={getattr(self, col)}')

        return f'<{self.__class__.__name__} {", ".join(cols)}>'