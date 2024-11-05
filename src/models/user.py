from sqlalchemy import String, Integer, Column, ForeignKey, Boolean, text, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, int_pk, str_uniq



class UserModel(BaseModel):
    __tablename__ = 'user'

    id: Mapped[int_pk]
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    password: Mapped[bytes] = mapped_column(LargeBinary)
    email: Mapped[str] = mapped_column(String(70), nullable=True, unique=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey('company.id'))

    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text('false'))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text('true'))

    company: Mapped[int] = relationship('CompanyModel', back_populates='users')
