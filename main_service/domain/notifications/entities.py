from dataclasses import dataclass
from datetime import datetime

from domain.notifications.enums import (
    NotificationTypeEnum,
    NotificationFormatEnum,
)


@dataclass
class Notification:
    text: str
    id: int | None = None
    recipient_id: int = 0
    type: NotificationTypeEnum = NotificationTypeEnum.EMAIL
    format: NotificationFormatEnum = NotificationFormatEnum.RAW_TEXT
    created_at: datetime | None = None
