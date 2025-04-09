from datetime import datetime

from infrastructure.api.models import CamelModel


class EventModel(CamelModel):
    title: str
    created_at: datetime
    start_date: datetime

    id: int
    is_visible: bool
    description: str | None

    end_date: datetime | None
    end_registration: datetime | None = None
