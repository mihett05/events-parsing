from dataclasses import dataclass
from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


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


class MailModel(CamelModel):
    id: int
    theme: str
    sender: str
    received_date: date

    raw_content: bytes

    attachments: list[str]


class DatesInfoModel(CamelModel):
    start_date: str
    end_date: str | None
    end_registration: str | None


class EventInfoModel(CamelModel):
    mail_id: int | None
    title: str
    description: str | None
    dates: DatesInfoModel
    type: EventTypeEnum
    format: EventFormatEnum
    location: str | None
    organization_name: str | None


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
