from dataclasses import dataclass

from domain.mails.enums import MailStateEnum


@dataclass
class UpdateMailDto:
    id: int
    state: MailStateEnum
    event_id: int | None = None
