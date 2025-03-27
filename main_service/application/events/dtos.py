from dataclasses import dataclass
from datetime import datetime, time

from domain.events.enums import WeekDayEnum


@dataclass
class UpdateEventDto:
    event_id: int
    title: str
    members: list[int]


@dataclass
class SetEventPermissionsDto:
    owner_id: int
    admins: list[int]


@dataclass
class MakeSingleEventDto:
    event_id: int
    start_date: datetime
    end_date: datetime


@dataclass
class MakeRepeatableEventDto:
    event_id: int
    start_time: time
    end_time: time
    start_day: WeekDayEnum
    end_day: WeekDayEnum
