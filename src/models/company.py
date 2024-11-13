from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, relationship

from .base import BaseModel, uuid_pk


class CompanyModel(BaseModel):
    __tablename__ = "company"

    id: Mapped[uuid_pk]
    inn: Mapped[int]
    company_name: Mapped[str] = Column(String(256))
    # admin_id: Mapped[UUID4] = Column(UUID, ForeignKey('user.id'))
    # user_id: Mapped[UUID4] = Column(UUID, ForeignKey('user.id'))
    # own_company = relationship(UserModel, backref='admin', uselist=False, foreign_keys=[admin_id])

    users = relationship(
        "UserModel",
        # foreign_keys="UserModel.company_id",
        back_populates="company",
    )
