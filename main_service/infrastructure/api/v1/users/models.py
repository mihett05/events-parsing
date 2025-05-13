from datetime import datetime

from domain.users.enums import UserNotificationSendToEnum

from infrastructure.api.models import CamelModel


class UserSettingsModel(CamelModel):
    id: int
    user_id: int
    type: UserNotificationSendToEnum


class UserModel(CamelModel):
    id: int
    email: str

    fullname: str
    is_active: bool

    telegram_id: int | None
    created_at: datetime
