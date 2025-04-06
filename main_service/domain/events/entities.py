from dataclasses import dataclass
from datetime import datetime, time

from domain.events.enums import WeekDayEnum


@dataclass
class EventSingle:
    event_id: int
    start_date: datetime
    end_date: datetime


@dataclass
class EventRepeatable:
    event_id: int
    start_time: time
    end_time: time
    start_day: WeekDayEnum
    end_day: WeekDayEnum


@dataclass
class Event:
    title: str
    start_date: datetime

    id: int | None = None
    is_visible: bool = True
    description: str | None = None

    end_date: datetime | None = None
    created_at: datetime | None = None
    end_registration: datetime | None = None
