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
