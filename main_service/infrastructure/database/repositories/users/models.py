from datetime import datetime

from domain.users.enums import UserNotificationSendToEnum
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
