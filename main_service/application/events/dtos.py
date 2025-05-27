from dataclasses import dataclass
from datetime import datetime

from domain.events.enums import EventFormatEnum, EventTypeEnum


@dataclass
class UpdateEventDto:
    """DTO для обновления параметров события."""

    event_id: int
    title: str
    description: str
    is_visible_status: bool | None = None
    # members: list[int] = field(default_factory=list[int])


@dataclass
class SetEventPermissionsDto:
    """DTO для установки прав доступа к событию."""

    owner_id: int
    admins: list[int]


@dataclass
class DatesInfo:
    """DTO с информацией о временных параметрах события."""

    start_date: datetime
    end_date: datetime | None
    end_registration: datetime | None


@dataclass
class EventInfo:
    """DTO с основной информацией о событии."""

    mail_id: int | None
    title: str
    description: str | None
    dates: DatesInfo
    type: EventTypeEnum
    format: EventFormatEnum
    location: str | None
    organization_name: str | None
    is_visible: bool = True
