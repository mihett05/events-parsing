from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from domain.mails.enums import MailStateEnum


@dataclass
class CreateMailDto:
    theme: str
    sender: str

    raw_content: bytes
    received_date: date
    state: MailStateEnum = MailStateEnum.UNPROCESSED
    retry_after: datetime = field(
        default_factory=lambda: datetime.now() + timedelta(minutes=30)
    )


@dataclass
class ReadAllMailsDto:
    page: int
    page_size: int
