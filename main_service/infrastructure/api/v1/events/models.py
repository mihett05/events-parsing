from datetime import datetime

from infrastructure.api.models import CamelModel


class EventModel(CamelModel):
    id: int
    title: str
    type: str
    format: str
    created_at: datetime
    organization_id: int | None = None

    is_visible: bool
    location: str | None
    description: str | None

    start_date: datetime
    end_date: datetime | None
    end_registration: datetime | None = None
    organization_id: int | None = None
