from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateOrganizationDto:
    owner_id: int
    title: str
    token: UUID


@dataclass
class ReadOrganizationsDto:
    page: int | None
    page_size: int | None
