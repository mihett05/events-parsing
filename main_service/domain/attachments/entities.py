from dataclasses import dataclass
from pathlib import Path
from uuid import UUID


@dataclass
class Attachment:
    """
    Part of model stores at Database (meta-data)
    Part of model stores at STORAGE (LOCAL/S3) (content)
    """

    id: UUID
    filename: str
    content: bytes | None = None

    @property
    def path(self) -> str:
        return f"{self.id}.{self.extension}"

    @property
    def extension(self) -> str:
        return Path(self.filename).suffix.lower()
