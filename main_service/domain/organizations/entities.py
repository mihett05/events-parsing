from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Organization:
    id: int
    created_at: datetime
    title: str
    owner_id: int


@dataclass
class OrganizationToken:
    id: UUID
    created_by: int
    used_by: int | None = None
    is_used: bool = False
