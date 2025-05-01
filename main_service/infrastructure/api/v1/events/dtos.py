from datetime import datetime

from pydantic import model_validator
from pydantic.v1 import root_validator

from infrastructure.api.models import CamelModel


class CreateEventModelDto(CamelModel):
    title: str
    type: str
    format: str
    location: str | None
    description: str | None
    end_date: datetime
    start_date: datetime
    end_registration: datetime
    organization_id: int | None

    @model_validator(mode="after")
    def check_dates_order(self):
        if self.start_date > self.end_date:
            raise ValueError("start_date must be less than or equal to end_date")
        return self


class UpdateEventModelDto(CamelModel):
    title: str
    description: str
    # members: list[int]
