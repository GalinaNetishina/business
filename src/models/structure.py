from pydantic import UUID4
from sqlalchemy import func, Column, Index, Integer, ForeignKey, UUID, Sequence
from sqlalchemy.orm import Mapped, relationship, foreign, remote
from sqlalchemy_utils import LtreeType, Ltree
from .base import BaseModel
from src.database import  get_session


id_seq = Sequence('position_id_seq')
class PositionModel(BaseModel):
    __tablename__ = "position"
    id =Column(Integer, primary_key=True)
    id = Column(Integer, id_seq, primary_key=True)
    name: Mapped[str]
    path = Column(LtreeType, nullable=True)
    company_id: Mapped[UUID4] = Column(UUID, ForeignKey("company.id"), nullable=True)
    company = relationship("CompanyModel", back_populates='positions')

    boss = relationship(
        "PositionModel",
        primaryjoin=remote(path) == foreign(func.subpath(path, 0, -1)),
        backref="subordinates",
        lazy="joined",
        viewonly=True
    )

    def __init__(self, name, parent=None):
            session = next(get_session())
            _id = session.execute(id_seq)
            self.id = _id
            self.name = name
            ltree_id = Ltree(str(_id))
            self.path = ltree_id if parent is None else parent.path + ltree_id
            session.commit()


    __table_args__ = (Index("ix_position_path", path, postgresql_using="gist"),)
