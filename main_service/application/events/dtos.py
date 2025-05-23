from dataclasses import dataclass
from datetime import datetime

from domain.events.enums import EventFormatEnum, EventTypeEnum


@dataclass
class UpdateEventDto:
    event_id: int
    title: str
    description: str
    # members: list[int] = field(default_factory=list[int])


@dataclass
class SetEventPermissionsDto:
    owner_id: int
    admins: list[int]


@dataclass
class DatesInfo:
    start_date: datetime
    end_date: datetime | None
    end_registration: datetime | None


@dataclass
class EventInfo:
    mail_id: int | None
    title: str
    description: str | None
    dates: DatesInfo
    type: EventTypeEnum
    format: EventFormatEnum
    location: str | None
    organization_name: str | None
