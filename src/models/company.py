from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column


from .base import BaseModel, uuid_pk


class CompanyModel(BaseModel):
    __tablename__ = "company"

    id: Mapped[uuid_pk]
    inn: Mapped[int] = mapped_column(Integer, unique=True)
    company_name: Mapped[str] = Column(String(256))
    structure: Mapped[list["StructureModel"]] = relationship(
        "StructureModel",
        back_populates="company",
        order_by='StructureModel.path'
    )

    # admin_id: Mapped[UUID | None] = mapped_column(ForeignKey('user.id'))
    # user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'), nullable=True)
    # admin = relationship(
    #     'UserModel',
    #     backref='own_company',
    #     uselist=False,
    #     foreign_keys=[admin_id]
    # )
    users = relationship("UserModel", viewonly=True)
