from datetime import datetime

from domain.notifications.enums import (
    NotificationFormatEnum,
    NotificationStatusEnum,
    NotificationTypeEnum,
)

from infrastructure.api.models import CamelModel


class NotificationModel(CamelModel):
    id: int
    created_at: datetime
    recipient_id: int

    text: str

    type: NotificationTypeEnum
    format: NotificationFormatEnum
    status: NotificationStatusEnum
