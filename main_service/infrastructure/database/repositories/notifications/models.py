from datetime import date, datetime

from domain.notifications.enums import (
    NotificationFormatEnum,
    NotificationStatusEnum,
)
from sqlalchemy import Date, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.postgres import Base


class NotificationDatabaseModel(Base):
    __tablename__ = "notifications"
    __table_args__ = (
        UniqueConstraint(
            "event_id", "recipient_id", "send_date", name="unique_notification"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    recipient_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    text: Mapped[str]
    send_date: Mapped[date] = mapped_column(Date, nullable=False)

    format: Mapped[NotificationFormatEnum] = mapped_column(
        ENUM(NotificationFormatEnum, name="NotificationFormatEnum")
    )
    status: Mapped[NotificationStatusEnum] = mapped_column(
        ENUM(NotificationStatusEnum, name="NotificationStatusEnum")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
