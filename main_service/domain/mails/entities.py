from dataclasses import dataclass
from datetime import datetime

from .enums import MailStateEnum


@dataclass
class Mail:
    theme: str
    sender: str

    raw_content: bytes
    state: MailStateEnum

    created_at: datetime = None

    id: int | None = None
    event_id: int | None = None
