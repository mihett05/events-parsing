from datetime import datetime

from domain.events.enums import (
    EventFormatEnum,
    EventTypeEnum,
)
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.postgres import Base
from infrastructure.database.repositories.attachments import (
    AttachmentDatabaseModel,
)
from infrastructure.database.repositories.users import UserDatabaseModel


class EventUserDatabaseModel(Base):
    __tablename__ = "event_users"

    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )


class EventDatabaseModel(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str]
    location: Mapped[str | None]
    description: Mapped[str | None] = mapped_column(nullable=True, default=None)
    is_visible: Mapped[bool] = mapped_column(default=True)
    organization_id: Mapped[int | None] = mapped_column(
        ForeignKey("organizations.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )

    type: Mapped[EventTypeEnum] = mapped_column(
        ENUM(EventTypeEnum, name="EventTypeEnum")
    )
    format: Mapped[EventFormatEnum] = mapped_column(
        ENUM(EventFormatEnum, name="EventFormatEnum")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    end_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None
    )
    end_registration: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None
    )
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    attachments: Mapped[list[AttachmentDatabaseModel]] = relationship(
        lazy="joined"
    )
    members: Mapped[list[UserDatabaseModel]] = relationship(
        UserDatabaseModel, lazy="select", secondary="event_users"
    )
