from domain.events.enums import EventFormatEnum, EventTypeEnum

from infrastructure.api.models import CamelModel


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
