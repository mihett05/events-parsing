from dataclasses import dataclass

from domain.users.entities import User


@dataclass
class CreateNotificationDto:
    chat_id: int
    text: str
    reply_to: int | None
    owner: User


@dataclass
class ReadNotificationsDto:
    chat_id: int
    page: int
    page_size: int
