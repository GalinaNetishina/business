from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    __abstract__ = True

    repr_cols_num = 3
    repr_cols = ()

    def __repr__(self) -> str:
        cols = []
        for col, _ in zip(self.__table__.columns.keys(), range(self.repr_cols_num)):
            cols.append(f'{col}={getattr(self, col)}')

        return f'<{self.__class__.__name__} {", ".join(cols)}>'