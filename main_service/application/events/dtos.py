from dataclasses import dataclass
from datetime import datetime, time

from domain.events.enums import WeekDayEnum


@dataclass
class UpdateEventDto:
    event_id: int
    title: str
    description: str
    # members: list[int] = field(default_factory=list[int])


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


@dataclass
class DatesInfo:
    start_date: datetime
    end_date: datetime | None
    end_registration: datetime | None


@dataclass
class EventInfo:
    mail_id: int | None
    title: str
    description: str | None
    dates: DatesInfo
    type: str
    format: str
    location: str | None
