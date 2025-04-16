from dataclasses import dataclass
from datetime import date, datetime

from domain.mails.enums import MailStateEnum


@dataclass
class CreateMailDto:
    theme: str
    sender: str

    raw_content: bytes
    received_date: date
    state: MailStateEnum = MailStateEnum.UNPROCESSED


@dataclass
class ReadAllMailsDto:
    page: int
    page_size: int
