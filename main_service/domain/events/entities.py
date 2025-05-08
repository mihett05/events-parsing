from dataclasses import dataclass, field
from datetime import datetime

from domain.users.entities import User


@dataclass
class Event:
    type: str
    title: str
    format: str
    location: str | None
    start_date: datetime

    id: int | None = None
    organization_id: int | None = None
    is_visible: bool = True
    description: str | None = None

    created_at: datetime | None = None
    end_date: datetime | None = None
    end_registration: datetime | None = None

    members: list[User] = field(default_factory=list)
