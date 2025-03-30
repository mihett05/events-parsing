from datetime import datetime

from sqlalchemy import func, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.postgres import Base


class EventDbModel(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    title: Mapped[str]
    description: Mapped[str]
    is_visible: Mapped[bool]
