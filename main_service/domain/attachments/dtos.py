from dataclasses import dataclass, field
from parser.events import Event
from typing import BinaryIO
from uuid import UUID, uuid4

from domain.mails.entities import Mail


@dataclass
class CreateAttachmentDto:
    filename: str
    extension: str
    content: BinaryIO
    mail: Mail | None = None
    event: Event | None = None
    id: UUID = field(default_factory=uuid4)
