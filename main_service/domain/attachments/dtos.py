from dataclasses import dataclass, field
from typing import BinaryIO
from uuid import UUID, uuid4

from domain.events.entities import Event
from domain.mails.entities import Mail


@dataclass
class ParsedAttachmentInfoDto:
    filename: str
    extension: str
    content: BinaryIO

    @property
    def file_path(self) -> str:
        return self.filename + self.extension


@dataclass
class CreateAttachmentDto:
    filename: str
    extension: str
    content: BinaryIO
    mail: Mail | None = None
    event: Event | None = None
    id: UUID = field(default_factory=uuid4)
