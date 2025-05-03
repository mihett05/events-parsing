from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EventTypeEnum(Enum):
    HACKATHON = "Хакатон"
    CONFERENCE = "Конференция"
    CONTEST = "Контест"
    OTHER = "Другое"


class EventFormatEnum(Enum):
    ONLINE = "Дистанционно"
    OFFLINE = "Очно"
    MIXED = "Смешанное"
    OTHER = "Другое"


@dataclass
class DatesInfo:
    start_date: str | None
    end_date: str | None
    end_registration: str | None


@dataclass
class EventInfo:
    mail_id: int | None
    title: str
    description: str | None
    dates: DatesInfo
    type: EventTypeEnum
    format: EventFormatEnum
    location: str | None
    organization_name: str | None


@dataclass
class Event:
    title: str
    location: str | None
    start_date: datetime

    type: EventTypeEnum = EventTypeEnum.OTHER
    format: EventFormatEnum = EventFormatEnum.OTHER

    id: int | None = None
    is_visible: bool = True
    description: str | None = None

    end_date: datetime | None = None
    created_at: datetime | None = None
    end_registration: datetime | None = None
