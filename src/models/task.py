from sqlalchemy import String, Enum, ForeignKey, UUID, text, JSON
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, relationship, mapped_column

from . import UserModel
from .base import BaseModel, uuid_pk, created_at, updated_at

from src.utils.enums import Statuses, Priorities


class TaskModel(BaseModel):
    __tablename__ = "task"

    id: Mapped[uuid_pk]
    title: Mapped[str]
    importance: Mapped[Priorities] = mapped_column(
        default=Priorities.STANDARD,
        server_default=text("'STANDARD'"),
    )
    status: Mapped[Statuses] = mapped_column(
        Enum(Statuses),
        default=Statuses.CREATED,
        server_default=text("'CREATED'"),
    )
    details: Mapped[str | None]
    tags: Mapped[list[str]] = mapped_column(ARRAY(String))
    start_data: Mapped[created_at]
    update_data: Mapped[updated_at]
    additional: Mapped[dict | None] = mapped_column(JSON)

    observer_id: Mapped[UUID | None] = mapped_column(ForeignKey("user.id"))
    performer_id: Mapped[UUID | None] = mapped_column(ForeignKey("user.id"))
    observer: Mapped["UserModel"] = relationship(
        "UserModel",
        backref="observed_tasks",
        foreign_keys=[observer_id],
        uselist=False,
        lazy="joined",
    )
    performer: Mapped["UserModel"] = relationship(
        "UserModel",
        backref="performed_tasks",
        foreign_keys=[performer_id],
        uselist=False,
    )
