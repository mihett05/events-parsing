from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class CreateEventDto:
    title: str
    type: str
    format: str
    location: str | None
    description: str | None
    organization_id: int | None
    end_date: datetime
    start_date: datetime
    end_registration: datetime


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
