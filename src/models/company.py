from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import Mapped, relationship

from .base import BaseModel
from .user import UserModel


class CompanyModel(BaseModel):
    __tablename__ = "company"

    id: Mapped[int] = Column(Integer, primary_key=True)
    inn: Mapped[int]
    company_name: Mapped[str] = Column(String(256))

    users: Mapped[list["UserModel"]] = relationship(UserModel, back_populates="company")
