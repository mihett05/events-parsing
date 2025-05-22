from datetime import datetime
from uuid import UUID

from domain.users.enums import RoleEnum, UserNotificationSendToEnum
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.postgres import Base


class UserSettingsDatabaseModel(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    type: Mapped[UserNotificationSendToEnum] = mapped_column(
        ENUM(UserNotificationSendToEnum, name="UserNotificationSendToEnum"),
        default=UserNotificationSendToEnum.EMAIL,
    )


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

    settings: Mapped[UserSettingsDatabaseModel] = relationship(
        cascade="all, delete-orphan", uselist=False
    )


class UserOrganizationRoleDatabaseModel(Base):
    __tablename__ = "user_organization_role"

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    role: Mapped[RoleEnum] = mapped_column(
        ENUM(RoleEnum, name="RoleEnum"), nullable=False
    )


class TelegramTokenDatabaseModel(Base):
    __tablename__ = "telegram_tokens"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    is_used: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class UserActivationTokenDatabaseModel(Base):
    __tablename__ = "user_activation_token"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"), default=None, nullable=True
    )

    user: Mapped[UserDatabaseModel] = relationship(
        "UserDatabaseModel", uselist=False
    )

    is_used: Mapped[bool] = mapped_column(default=False)
