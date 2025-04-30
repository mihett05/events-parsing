from datetime import datetime

from domain.notifications.enums import (
    NotificationFormatEnum,
    NotificationStatusEnum,
)

from infrastructure.api.models import CamelModel


class NotificationModel(CamelModel):
    id: int
    created_at: datetime
    recipient_id: int

    text: str

    format: NotificationFormatEnum
    status: NotificationStatusEnum
