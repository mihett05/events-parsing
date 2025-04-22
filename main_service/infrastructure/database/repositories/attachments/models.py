from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.postgres import Base


class AttachmentDatabaseModel(Base):
    __tablename__ = "attachments"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    filename: Mapped[str]

    owner_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    event_id: Mapped[int | None] = mapped_column(
        ForeignKey("events.id"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
