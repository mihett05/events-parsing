from dataclasses import dataclass, field
from datetime import date, datetime

from domain.attachments.entities import Attachment
from domain.events.enums import EventFormatEnum, EventTypeEnum
from domain.users.entities import User


@dataclass
class EventUser:
    event_id: int
    user_id: int


@dataclass
class Event:
    title: str
    location: str | None
    start_date: date

    type: EventTypeEnum = EventTypeEnum.OTHER
    format: EventFormatEnum = EventFormatEnum.OTHER

    id: int | None = None
    organization_id: int | None = None
    is_visible: bool = True
    description: str | None = None

    created_at: datetime | None = None
    end_date: date | None = None
    end_registration: date | None = None

    attachments: list[Attachment] = field(default_factory=list)
    members: list[User] = field(default_factory=list)
