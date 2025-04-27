from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Attachment:
    """
    Part of model stores at Database (meta-data)
    Part of model stores at STORAGE (LOCAL/S3) (content)
    """

    id: UUID
    filename: str
    extension: str
    file_link: str | None = None

    mail_id: int | None = None
    event_id: int | None = None
    created_at: datetime | None = None

    @property
    def path(self) -> str:
        return f"{self.id}{self.extension}"
