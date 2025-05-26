from datetime import datetime

from domain.events.enums import EventFormatEnum, EventTypeEnum
from domain.events.exceptions import InvalidEventPeriodError
from pydantic import BaseModel, model_validator

from infrastructure.api.models import CamelModel


def _check_dates_order(self):
    if self.start_date is None or self.end_date is None:
        return self

    if self.start_date > self.end_date:
        raise InvalidEventPeriodError()
    return self


class CreateEventModelDto(CamelModel):
    title: str
    type: EventTypeEnum
    format: EventFormatEnum
    location: str | None
    description: str | None
    end_date: datetime
    start_date: datetime
    end_registration: datetime
    organization_id: int | None
    is_visible: bool = True

    @model_validator(mode="after")
    def _check_dates_period(self):
        return _check_dates_order(self)


class UpdateEventModelDto(CamelModel):
    title: str
    description: str
    is_visible_status: bool


class ReadAllEventsFeedModelDto(BaseModel):
    page: int = 0
    page_size: int = 50
    organization_id: int | None = None
    type: EventTypeEnum | None = None
    format: EventFormatEnum | None = None
    end_date: datetime | None = None
    start_date: datetime | None = None

    @model_validator(mode="after")
    def _check_dates_period(self):
        return _check_dates_order(self)


class ReadAllEventsCalendarModelDto(BaseModel):
    end_date: datetime | None = None
    start_date: datetime | None = None

    @model_validator(mode="after")
    def _check_dates_period(self):
        return _check_dates_order(self)
