from dataclasses import dataclass, field
from datetime import datetime, timedelta

from domain.mails.enums import MailStateEnum


@dataclass
class UpdateMailDto:
    id: int
    state: MailStateEnum
    event_id: int | None = None
