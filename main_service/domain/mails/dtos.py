from dataclasses import dataclass
from datetime import datetime

from domain.mails.enums import MailStateEnum


@dataclass
class CreateMailDto:
    theme: str
    sender: str

    raw_content: bytes
    created_at: datetime
    state: MailStateEnum = MailStateEnum.UNPROCESSED


@dataclass
class ReadAllMailsDto:
    page: int
    page_size: int
