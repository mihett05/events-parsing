from datetime import date, datetime

from domain.mails.enums import MailStateEnum
from sqlalchemy import Date, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.postgres import Base
from infrastructure.database.repositories.attachments import (
    AttachmentDatabaseModel,
)


class MailDatabaseModel(Base):
    """
    Модель для представления электронных писем в базе данных.

    Содержит метаданные письма, его содержимое и состояние обработки.
    Поддерживает связь с событиями через event_id и может содержать вложения.
    """

    __tablename__ = "mails"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id", ondelete="SET NULL"), nullable=True
    )

    received_date: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    retry_after: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    theme: Mapped[str]
    sender: Mapped[str]
    raw_content: Mapped[bytes]
    state: Mapped[MailStateEnum] = mapped_column(
        ENUM(MailStateEnum, name="MailStateEnum")
    )

    attachments: Mapped[list[AttachmentDatabaseModel]] = relationship(lazy="joined")
