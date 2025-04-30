from datetime import datetime

from domain.notifications.enums import (
    NotificationFormatEnum,
    NotificationStatusEnum,
    NotificationTypeEnum,
)
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.postgres import Base


class NotificationDatabaseModel(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipient_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )

    text: Mapped[str]

    type: Mapped[NotificationTypeEnum] = mapped_column(
        ENUM(NotificationTypeEnum, name="NotificationTypeEnum")
    )
    format: Mapped[NotificationFormatEnum] = mapped_column(
        ENUM(NotificationFormatEnum, name="NotificationFormatEnum")
    )
    status: Mapped[NotificationStatusEnum] = mapped_column(
        ENUM(NotificationStatusEnum, name="NotificationStatusEnum")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
