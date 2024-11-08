from sqlalchemy import String, Integer, Column, ForeignKey, Boolean, text, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, uuid_pk



class UserModel(BaseModel):
    __tablename__ = 'user'

    id: Mapped[uuid_pk]
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    password: Mapped[bytes] = mapped_column(LargeBinary)
    email: Mapped[str | None] = mapped_column(String(70), unique=True)
    company_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('company.id'))

    is_admin: Mapped[bool | None] = mapped_column(Boolean, default=False, server_default=text('false'))
    is_active: Mapped[bool | None] = mapped_column(Boolean, default=True, server_default=text('true'))

    company: Mapped[int] = relationship('CompanyModel', back_populates='users')
