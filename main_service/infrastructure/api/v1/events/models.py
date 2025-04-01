from datetime import datetime

from infrastructure.api.models import CamelModel


class EventModel(CamelModel):
    id: int
    title: str
    description: str

    is_visible: bool
    created_at: datetime

    end_date: datetime
    start_date: datetime
