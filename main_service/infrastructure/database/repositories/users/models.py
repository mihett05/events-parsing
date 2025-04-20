from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.postgres import Base


class UserDatabaseModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)

    fullname: Mapped[str] = mapped_column(nullable=True, default="")
    is_active: Mapped[bool] = mapped_column(default=True)

    salt: Mapped[str]
    hashed_password: Mapped[str]

    telegram_id: Mapped[int | None] = mapped_column(unique=True, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
