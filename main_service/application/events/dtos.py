from dataclasses import dataclass
from datetime import datetime, time

from application.auth.enums import PermissionsEnum
from domain.events.enums import WeekDayEnum


@dataclass
class UpdateEventDto:
    event_id: int
    title: str
    members: tuple[int]


@dataclass
class SetEventPermissionDto:
    event_id: int
    permissions: tuple[int, tuple[PermissionsEnum]]


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
