from datetime import datetime

from infrastructure.api.models import CamelModel


class CreateEventModelDto(CamelModel):
    title: str
    type: str
    format: str
    description: str
    organization_id: int
    end_date: datetime
    start_date: datetime
    end_registration: datetime


class UpdateEventModelDto(CamelModel):
    title: str
    description: str
    # members: list[int]
