from datetime import date

from domain.events.enums import EventFormatEnum, EventTypeEnum

from infrastructure.api.models import CamelModel


class MailModel(CamelModel):
    """Pydantic модель для представления данных о письме."""

    id: int
    theme: str
    sender: str
    received_date: date

    raw_content: bytes

    attachments: list[str]


class DatesInfoModel(CamelModel):
    """Pydantic модель для представления информации о датах события."""

    start_date: str
    end_date: str | None
    end_registration: str | None


class EventInfoModel(CamelModel):
    """Pydantic модель для представления полной информации о событии."""

    mail_id: int | None
    title: str
    description: str | None
    dates: DatesInfoModel
    type: EventTypeEnum
    format: EventFormatEnum
    location: str | None
    organization_name: str | None
    is_visible: bool
