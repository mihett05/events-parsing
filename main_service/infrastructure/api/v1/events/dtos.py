from datetime import datetime

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
    organization_id: int


class UpdateEventModelDto(CamelModel):
    title: str
    description: str
    # members: list[int]
