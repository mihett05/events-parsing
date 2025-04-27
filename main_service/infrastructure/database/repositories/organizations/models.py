from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Table,
    func,
    Enum as SQLEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.postgres import Base
from infrastructure.database.repositories.organizations.enums import (
    UserRoleEnum,
)

association_table = Table(
    "association_table",
    Base.metadata,
    Column("organization_id", ForeignKey("organizations.id")),
    Column("user_id", ForeignKey("users.id")),
    Column("role", SQLEnum(UserRoleEnum), nullable=False),
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

    title: Mapped[str]
