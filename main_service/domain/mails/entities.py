from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from .enums import MailStateEnum


@dataclass
class Mail:
    theme: str
    sender: str
    received_date: date

    raw_content: bytes
    retry_after: datetime
    state: MailStateEnum

    created_at: datetime = None
    id: int | None = None
    event_id: int | None = None
