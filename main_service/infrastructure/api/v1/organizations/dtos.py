from datetime import datetime

from infrastructure.api.models import CamelModel


class CreateOrganizationModelDto(CamelModel):
    title: str
    created_at: datetime


class UpdateOrganizationModelDto(CamelModel):
    title: str
