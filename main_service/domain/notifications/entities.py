from dataclasses import dataclass
from datetime import date, datetime

from domain.notifications.enums import (
    NotificationFormatEnum,
    NotificationStatusEnum,
)


@dataclass
class Notification:
    text: str
    event_id: int
    recipient_id: int
    send_date: date

    id: int | None = None
    format: NotificationFormatEnum = NotificationFormatEnum.RAW_TEXT
    status: NotificationStatusEnum = NotificationStatusEnum.UNSENT
    created_at: datetime | None = None
