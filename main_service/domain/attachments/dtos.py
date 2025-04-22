from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class CreateAttachmentDto:
    filename: str
    content: bytes
    id: UUID = field(default_factory=UUID)
