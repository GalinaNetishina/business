from sqlalchemy import func, Column, Index
from sqlalchemy.orm import Mapped, relationship, foreign, remote
from sqlalchemy_utils import LtreeType, Ltree
from .base import BaseModel, uuid_pk

# class StructureModel(BaseModel):
#     __tablenamae__ = "structure"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     company_id = mapped_column(UUID, ForeignKey('company.id'))
#     positions: Mapped['PositionModel'] = mapped_column()


class PositionModel(BaseModel):
    __tablename__ = "position"
    id: Mapped[uuid_pk]
    name: Mapped[str]
    path = Column(LtreeType, nullable=True)

    boss = relationship(
        "PositionModel",
        primaryjoin=remote(path) == foreign(func.subpath(path, 0, -1)),
        backref="subordinates",
    )

    def __init__(self, name, parent=None):
        self.name = name
        ltree_id = Ltree(str(self.id))
        self.path = ltree_id if parent is None else parent.path + ltree_id

    __table_args__ = (Index("ix_positions_path", path, postgresql_using="gist"),)
