from pydantic import UUID4
from sqlalchemy import func, Column, Index, Integer, ForeignKey, UUID
from sqlalchemy.orm import Mapped, relationship, foreign, remote, mapped_column
from sqlalchemy_utils import LtreeType, Ltree
from .base import BaseModel


# company_positions_at=Table(
#     "structure",
#     BaseModel.metadata,
#     Column('id', Integer, primary_key=True),
#     Column('company_id', ForeignKey("company.id"), nullable=False),
#     Column('position_id', ForeignKey("position.id"), nullable=False),
#     UniqueConstraint('company_id', 'position_id', name='idx_uniq_company_position')
# )
class StructureModel(BaseModel):
    __tablename__ = "structure"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[UUID4] = Column(UUID, ForeignKey("company.id"), nullable=True)
    position_id: Mapped[list[int]] = Column(
        Integer, ForeignKey("position.id"), nullable=True
    )
    # company = relationship('CompanyModel', uselist=False, back_populates='structure')
    # positions = relationship("PositionModel", back_populates='structure')


class PositionModel(BaseModel):
    __tablename__ = "position"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    path = Column(LtreeType, nullable=True)
    company_id: Mapped[UUID4] = Column(UUID, ForeignKey("company.id"), nullable=True)
    company = relationship("CompanyModel")

    boss = relationship(
        "PositionModel",
        primaryjoin=remote(path) == foreign(func.subpath(path, 0, -1)),
        backref="subordinates",
        lazy="joined",
    )

    def __init__(self, name, parent=None):
        self.name = name
        ltree_id = Ltree(str(self.name))
        self.path = ltree_id if parent is None else parent.path + ltree_id

    __table_args__ = (Index("ix_positions_path", path, postgresql_using="gist"),)
