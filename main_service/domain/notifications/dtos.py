from dataclasses import dataclass
from datetime import date

from domain.notifications.enums import (
    NotificationFormatEnum,
    NotificationStatusEnum,
)


@dataclass
class CreateNotificationDto:
    text: str
    event_id: int
    recipient_id: int
    send_date: date
    format: NotificationFormatEnum
    status: NotificationStatusEnum


@dataclass
class ReadNotificationsDto:
    page: int
    page_size: int
    send_date: date
    for_update: bool
