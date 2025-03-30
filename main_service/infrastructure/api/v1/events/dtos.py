from datetime import datetime

from infrastructure.api.models import CamelModel


class CreateEventModelDto(CamelModel):
    title: str
    description: str
    organization_id: int
    start_date: datetime
    end_date: datetime


class UpdateEventModelDto(CamelModel):
    title: str
    description: str
    # members: list[int]
