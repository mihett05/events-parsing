from dataclasses import dataclass
from datetime import datetime

from domain.events.enums import EventFormatEnum, EventTypeEnum


@dataclass
class Event:
    title: str
    location: str | None
    start_date: datetime
    type: EventTypeEnum = EventTypeEnum.OTHER
    format: EventFormatEnum = EventFormatEnum.OTHER
    id: int | None = None
    organization_id: int | None = None
    is_visible: bool = True
    description: str | None = None
    end_date: datetime | None = None
    created_at: datetime | None = None
    end_registration: datetime | None = None
