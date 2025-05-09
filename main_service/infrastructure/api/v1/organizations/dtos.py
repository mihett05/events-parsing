from uuid import UUID

from infrastructure.api.models import CamelModel


class CreateOrganizationModelDto(CamelModel):
    title: str
    token: UUID


class UpdateOrganizationModelDto(CamelModel):
    title: str
