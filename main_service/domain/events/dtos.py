from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateEventDto:
    title: str
    organization_id: int
    start_date: datetime
    end_date: datetime


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
