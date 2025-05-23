from dataclasses import dataclass
from datetime import date, datetime

from domain.events.enums import EventFormatEnum, EventTypeEnum


@dataclass
class CreateEventDto:
    title: str
    description: str | None
    start_date: datetime
    end_date: datetime
    end_registration: datetime
    location: str | None
    type: EventTypeEnum = EventTypeEnum.OTHER
    format: EventFormatEnum = EventFormatEnum.OTHER
    organization_id: int | None = None


@dataclass
class ReadUserEventsDto:
    user_id: int
    page: int
    page_size: int


@dataclass
class ReadOrganizationEventsDto:
    organization_id: int
    page: int
    page_size: int


@dataclass
class ReadAllEventsDto:
    start_date: date | None
    end_date: date | None


@dataclass
class ReadAllEventsFeedDto:
    page: int
    page_size: int
    start_date: date | None
    end_date: date | None
    organization_id: int | None
    type: EventTypeEnum | None
    format: EventFormatEnum | None
