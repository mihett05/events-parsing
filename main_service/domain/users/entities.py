from dataclasses import dataclass
from datetime import datetime

from domain.users.enums import UserNotificationSendToEnum


@dataclass
class UserSettings:
    id: int
    user_id: int
    type: UserNotificationSendToEnum = UserNotificationSendToEnum.EMAIL


@dataclass
class User:
    email: str

    fullname: str

    id: int | None = None
    is_active: bool = True

    salt: str = None
    hashed_password: str = None

    telegram_id: int | None = None
    created_at: datetime = None
    settings: UserSettings = None
