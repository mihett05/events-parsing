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
    description: str

    end_date: datetime
    start_date: datetime
    end_registration: datetime

    id: int | None = None
    created_at: datetime = None
    is_visible: bool = True
