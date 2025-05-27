from datetime import datetime
from uuid import UUID

from domain.users.enums import RoleEnum, UserNotificationSendToEnum
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.postgres import Base


class UserSettingsDatabaseModel(Base):
    """
    Модель базы данных для хранения настроек пользователя.
    Включает предпочтительный способ получения уведомлений и идентификатор календаря.
    """

    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    type: Mapped[UserNotificationSendToEnum] = mapped_column(
        ENUM(UserNotificationSendToEnum, name="UserNotificationSendToEnum"),
        default=UserNotificationSendToEnum.EMAIL,
    )
    calendar_uuid: Mapped[UUID | None] = mapped_column(nullable=True, default=None)


class UserDatabaseModel(Base):
    """
    Основная модель пользователя в базе данных.
    Содержит учетные данные, контактные данные и настройки пользователя.
    """

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
    """
    Модель для хранения ролей пользователей в организациях.
    Реализует связь многие-ко-многим между пользователями и организациями.
    """

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
    """
    Модель для хранения токенов привязки Telegram-аккаунтов.
    Содержит информацию о использовании и времени создания токена.
    """

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
    """
    Модель для хранения токенов активации пользователей.
    Связана с пользователем и содержит статус использования токена.
    """

    __tablename__ = "user_activation_tokens"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"), default=None, nullable=True
    )

    user: Mapped[UserDatabaseModel] = relationship("UserDatabaseModel", uselist=False)

    is_used: Mapped[bool] = mapped_column(default=False)
