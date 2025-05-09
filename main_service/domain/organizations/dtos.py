from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class CreateOrganizationDto:
    owner_id: int
    title: str
    token: UUID


@dataclass
class ReadOrganizationsDto:
    page: int | None
    page_size: int | None


@dataclass
class CreateOrganizationTokenDto:
    created_by: int
    id: UUID = field(default_factory=uuid4)


@dataclass
class ReadOrganizationTokensDto:
    created_by: int
    page: int
    page_size: int
