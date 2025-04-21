from datetime import datetime

from infrastructure.api.models import CamelModel


class CreateOrganizationModelDto(CamelModel):
    title: str
    description: str
    id: int
    admins_id: list[int]
    members_id: list[int]
    create_at: datetime


class UpdateOrganizationModelDto(CamelModel):
    title: str
    description: str
