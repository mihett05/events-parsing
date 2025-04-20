from datetime import datetime

from infrastructure.api.models import CamelModel


class OrganizationModel(CamelModel):
    title: str
    created_at: datetime

    id: int
    id_admin: int
    description: str | None
