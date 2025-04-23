from dataclasses import dataclass

from domain.notifications.enums import (
    NotificationTypeEnum,
    NotificationFormatEnum,
)


@dataclass
class CreateNotificationDto:
    recipient_id: int
    text: str
    type: NotificationTypeEnum
    format: NotificationFormatEnum


@dataclass
class ReadNotificationsDto:
    page: int
    page_size: int
