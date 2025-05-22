from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from domain.users.enums import RoleEnum, UserNotificationSendToEnum


@dataclass
class UserSettings:
    # Кринж
    id: int = None
    user_id: int = None
    type: UserNotificationSendToEnum = UserNotificationSendToEnum.EMAIL

    @classmethod
    def get_default(cls) -> "UserSettings":
        return UserSettings()


@dataclass
class User:
    email: str

    fullname: str

    id: int | None = None
    is_active: bool = True

    # TODO: cock dick blowjob
    salt: str = None
    hashed_password: str = None

    telegram_id: int | None = None
    created_at: datetime = None
    settings: UserSettings = field(default_factory=UserSettings.get_default)  # Тоже кринж


@dataclass
class UserOrganizationRole:
    organization_id: int
    user_id: int
    role: RoleEnum


@dataclass
class TelegramToken:
    id: UUID
    user_id: int
    is_used: bool = False
    created_at: datetime | None = None


@dataclass
class UserActivationToken:
    id: UUID
    user_id: int
    user: User
    is_used: bool = False
