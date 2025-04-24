from dataclasses import dataclass

from domain.notifications.enums import (
    NotificationFormatEnum,
    NotificationStatusEnum,
    NotificationTypeEnum,
)


@dataclass
class CreateNotificationDto:
    recipient_id: int
    text: str
    type: NotificationTypeEnum
    format: NotificationFormatEnum
    status: NotificationStatusEnum


@dataclass
class ReadNotificationsDto:
    page: int
    page_size: int
