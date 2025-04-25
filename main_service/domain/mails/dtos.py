from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from domain.attachments.dtos import CreateAttachmentDto, ParsedAttachmentInfoDto
from domain.mails.enums import MailStateEnum


@dataclass
class ParsedMailInfoDto:
    imap_mail_uid: str
    theme: str
    sender: str

    raw_content: bytes
    received_date: date
    attachments: list[ParsedAttachmentInfoDto] = field(default_factory=list)


@dataclass
class CreateMailDto:
    imap_mail_uid: str
    theme: str
    sender: str

    raw_content: bytes
    received_date: date
    attachments: list[CreateAttachmentDto] = field(default_factory=list)

    state: MailStateEnum = MailStateEnum.UNPROCESSED
    retry_after: datetime = field(
        default_factory=lambda: datetime.now() + timedelta(minutes=30)
    )


@dataclass
class ReadAllMailsDto:
    page: int
    page_size: int
