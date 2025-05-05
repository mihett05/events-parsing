from datetime import datetime

from domain.users.enums import RoleEnum
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import ENUM
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


class UserOrganizationRoleDatabaseModel(Base):
    __tablename__ = "user_organization_role"

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True
    )
    role: Mapped[RoleEnum] = mapped_column(
        ENUM(RoleEnum, name="RoleEnum"), nullable=False
    )
