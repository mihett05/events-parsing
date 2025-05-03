from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateOrganizationDto:
    owner_id: int
    title: str
    created_at: datetime


@dataclass
class ReadOrganizationsDto:
    page: int | None
    page_size: int | None
