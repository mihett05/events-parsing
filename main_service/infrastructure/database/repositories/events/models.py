from datetime import datetime

from domain.events.enums import (
    EventFormatEnum,
    EventTypeEnum,
)
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.postgres import Base


class EventDatabaseModel(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    end_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None
    )
    end_registration: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None
    )

    type: Mapped[EventTypeEnum] = mapped_column(
        ENUM(EventTypeEnum, name="EventTypeEnum")
    )
    title: Mapped[str]
    format: Mapped[EventFormatEnum] = mapped_column(
        ENUM(EventFormatEnum, name="EventFormatEnum")
    )
    location: Mapped[str | None]

    description: Mapped[str | None] = mapped_column(nullable=True, default=None)
    is_visible: Mapped[bool] = mapped_column(default=True)
    organization_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True, default=None
    )
