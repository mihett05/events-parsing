from datetime import datetime

from domain.events.enums import EventFormatEnum, EventTypeEnum

from infrastructure.api.models import CamelModel
from infrastructure.api.v1.organizations.models import OrganizationModel


class EventModel(CamelModel):
    id: int
    title: str
    type: EventTypeEnum
    format: EventFormatEnum
    created_at: datetime

    is_visible: bool
    location: str | None
    description: str | None

    start_date: datetime
    end_date: datetime | None
    end_registration: datetime | None = None
    organization_id: int | None = None


class FilterModel(CamelModel):
    type: list[EventTypeEnum]
    format: list[EventFormatEnum]
    organization: list[OrganizationModel]
