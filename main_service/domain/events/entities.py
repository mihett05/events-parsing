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
    id: int
    title: str

    organization_id: int | None  # None for personal events

    owner_id: int
    admins: set[int]  # Empty for personal events
    members: set[int]  # Empty for personal events

    single: EventSingle | None
    repeatable: EventRepeatable | None

    is_visible: bool = True
