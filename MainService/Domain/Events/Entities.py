from dataclasses import dataclass
from datetime import datetime, time

from MainService.Domain.Events.Enums import WeekDayEnum


@dataclass
class EventSingle:
    event_id: int
    start_date: datetime
    end_date: datetime

@dataclass
class EventRepitable:
    event_id: int
    start_time: time
    end_time: time
    start_day: WeekDayEnum
    end_day: WeekDayEnum

@dataclass
class Event:
    id: int
    title: str
    organization_id: int
    members: list[int]
    single: EventSingle | None
    repitable: EventRepitable | None