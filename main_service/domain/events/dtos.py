from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateEventDto:
    title: str
    type: str
    format: str
    location: str | None
    description: str | None
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
    page: int
    page_size: int
    start_date: datetime | None
    end_date: datetime | None
