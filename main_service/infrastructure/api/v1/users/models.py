from datetime import datetime
from uuid import UUID

from domain.users.enums import RoleEnum, UserNotificationSendToEnum

from infrastructure.api.models import CamelModel


class UserSettingsModel(CamelModel):
    """
    Модель настроек пользователя для API.
    """

    id: int
    user_id: int
    type: UserNotificationSendToEnum
    calendar_uuid: UUID | None


class UserModel(CamelModel):
    """
    Модель пользователя для API.
    """

    id: int
    email: str

    fullname: str
    is_active: bool

    telegram_id: int | None
    created_at: datetime
    settings: UserSettingsModel


class UserRoleModel(CamelModel):
    """
    Модель роли пользователя в организации для API.
    """

    user_id: int
    organization_id: int

    role: RoleEnum


class PublicUserModel(CamelModel):
    id: int

    fullname: str
    is_active: bool
