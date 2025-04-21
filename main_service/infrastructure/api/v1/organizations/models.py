from datetime import datetime

from infrastructure.api.models import CamelModel


class OrganizationModel(CamelModel):
    title: str
    created_at: datetime

    id: int
    owner_id: int
    admins: list[int]
    description: str | None
