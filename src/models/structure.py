from sqlalchemy import func, Column, Index, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship, foreign, remote, mapped_column
from sqlalchemy_utils import LtreeType, Ltree
from .base import BaseModel, uuid_pk


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


class StructureModel(BaseModel):
    __tablename__ = "structure"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id = mapped_column(ForeignKey("company.id"))
    positions = mapped_column(ForeignKey("position.id"))
    # company = relationship('CompanyModel', uselist=False, back_populates='structure', lazy='joined')
    # users = relationship('UserModel', primaryjoin=company_id=='user.company_id')
    # admin_id: Mapped[UUID | None] = mapped_column(ForeignKey('user.id'))
    # admin = relationship(
    #     'UserModel',
    #     backref='own_company',
    #     uselist=False,
    #     foreign_keys=[admin_id]
    # )
