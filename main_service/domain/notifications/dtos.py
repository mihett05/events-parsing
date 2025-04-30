from dataclasses import dataclass

from domain.notifications.enums import (
    NotificationFormatEnum,
    NotificationStatusEnum,
)


@dataclass
class CreateNotificationDto:
    recipient_id: int
    text: str
    format: NotificationFormatEnum
    status: NotificationStatusEnum


@dataclass
class ReadNotificationsDto:
    page: int
    page_size: int
