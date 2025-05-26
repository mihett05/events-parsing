from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Organization:
    title: str
    owner_id: int
    id: int | None = None
    created_at: datetime | None = None


@dataclass
class OrganizationToken:
    id: UUID
    created_by: int
    used_by: int | None = None
    is_used: bool = False
