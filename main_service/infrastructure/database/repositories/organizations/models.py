from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.postgres import Base


association_table = Table(
    "association_table",
    Base.metadata,
    Column("left_id", ForeignKey("organizations.id")),
    Column("right_id", ForeignKey("users.id")),
)


class OrganizationDatabaseModel(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    admins: Mapped[list[int]] = relationship(secondary=association_table)
    title: Mapped[str]
    description: Mapped[str | None] = mapped_column(nullable=True, default=None)
