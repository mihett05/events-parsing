from dataclasses import dataclass
from datetime import datetime


@dataclass
class Organization:
    id: int
    created_at: datetime
    title: str
    owner_id: int
