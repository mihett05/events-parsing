from dataclasses import dataclass
from datetime import date, datetime

from .enums import MailStateEnum


@dataclass
class Mail:
    theme: str
    sender: str
    received_date: date

    raw_content: bytes
    state: MailStateEnum

    created_at: datetime = None
    ded_line: datetime = None
    id: int | None = None
    event_id: int | None = None
