from datetime import datetime
from uuid import UUID

from infrastructure.api.models import CamelModel


class AttachmentModel(CamelModel):
    """Pydantic модель для представления данных о вложении."""

    id: UUID
    filename: str
    extension: str
    created_at: datetime

    file_link: str

    mail_id: int | None = None
    event_id: int | None = None
