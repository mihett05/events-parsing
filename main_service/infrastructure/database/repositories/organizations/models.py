from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.postgres import Base


class OrganizationDatabaseModel(Base):
    """Модель организации в базе данных."""

    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET DEFAULT"),
        nullable=False,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    title: Mapped[str]


class OrganizationTokenDatabaseModel(Base):
    """Модель токена для доступа к организации."""

    __tablename__ = "organization_tokens"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    used_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), default=None, nullable=True
    )
    is_used: Mapped[bool] = mapped_column(default=False)
