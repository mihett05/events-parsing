from datetime import datetime

from pydantic import ValidationError, model_validator

from domain.events.enums import EventFormatEnum, EventTypeEnum
from infrastructure.api.models import CamelModel


class PeriodValidatorModel(CamelModel):
    end_date: datetime | None = None
    start_date: datetime | None = None

    def _check_dates_order(self):
        if self.start_date is None or self.end_date is None:
            return self

        if self.start_date > self.end_date:
            raise ValidationError(
                "start_date must be less than or equal to end_date"
            )
        return self


class CreateEventModelDto(PeriodValidatorModel):
    title: str
    type: EventTypeEnum
    format: EventFormatEnum
    location: str | None
    description: str | None
    end_date: datetime
    start_date: datetime
    end_registration: datetime
    organization_id: int | None
    
    @model_validator(mode="after")
    def _check_dates_order(self):
        super()._check_dates_order()


class UpdateEventModelDto(CamelModel):
    title: str
    description: str


class ReadAllEventsFeedModelDto(PeriodValidatorModel):
    page: int = 0
    page_size: int = 50
    organization_id: int | None
    type: EventTypeEnum | None
    format: EventFormatEnum | None

    @model_validator(mode="after")
    def _check_dates_order(self):
        super()._check_dates_order()


class ReadAllEventsCalendarModelDto(PeriodValidatorModel):
    @model_validator(mode="after")
    def _check_dates_order(self):
        super()._check_dates_order()
