from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.users.enums import RoleEnum, UserNotificationSendToEnum


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


@dataclass
class UserOrganizationRole:
    organization_id: int
    user_id: int
    role: RoleEnum


@dataclass
class UserActivationToken:
    id: UUID
    created_by: int
    user_id: int
    user: User
    is_used: bool = False
