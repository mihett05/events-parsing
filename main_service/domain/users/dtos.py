from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class ReadAllUsersDto:
    page: int
    page_size: int


@dataclass
class CreateTelegramTokenDto:
    user_id: int
    id: UUID = field(default_factory=uuid4)
