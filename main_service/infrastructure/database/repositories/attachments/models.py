from datetime import datetime
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.postgres import Base


class AttachmentDatabaseModel(Base):
    __tablename__ = "attachments"
    __table_args__ = (
        CheckConstraint(
            "mail_id is not null or event_id is not null", "attachment_links"
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)
    filename: Mapped[str]
    extension: Mapped[str]

    mail_id: Mapped[int | None] = mapped_column(
        ForeignKey("mails.id"),
        nullable=True,
    )
    event_id: Mapped[int | None] = mapped_column(ForeignKey("events.id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
