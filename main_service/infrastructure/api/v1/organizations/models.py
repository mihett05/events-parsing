from datetime import datetime
from uuid import UUID

from infrastructure.api.models import CamelModel


class OrganizationModel(CamelModel):
    """
    Модель организации для API.
    """

    id: int
    created_at: datetime
    title: str
    owner_id: int


class OrganizationTokenModel(CamelModel):
    """
    Модель токена организации для API.
    """

    id: UUID
    created_by: int
    used_by: int | None = None
    is_used: bool = False
