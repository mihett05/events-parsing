from dataclasses import dataclass

from MainService.Domain.User.Entities import User

@dataclass
class CreateNotificationDto:
    chat_id: int
    text: str
    reply_to: int | None
    owner: User

@dataclass
class ReadNotificationDto:
    chat_id: int
    page: int
    page_size: int