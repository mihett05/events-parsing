from datetime import datetime

from infrastructure.api.models import CamelModel


class CreateOrganizationModelDto(CamelModel):
    title: str
    description: str
    id: int
    id_admin: int
    create_at: datetime


class UpdateOrganizationModelDto(CamelModel):
    title: str
    description: str
    # members: list[int]
