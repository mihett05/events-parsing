from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    title: str
    start_date: datetime

    id: int | None = None
    is_visible: bool = True
    description: str | None = None

    end_date: datetime | None = None
    created_at: datetime | None = None
    end_registration: datetime | None = None

