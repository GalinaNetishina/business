from sqlalchemy import String, Integer, Column, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class UserModel(BaseModel):
    __tablename__ = 'user'

    id: Mapped[int] = Column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    email: Mapped[str] = mapped_column(String(70), nullable=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey('company.id'))
    company: Mapped[int] = relationship('CompanyModel', back_populates='users')
