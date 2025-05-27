from uuid import UUID

from infrastructure.api.models import CamelModel


class CreateOrganizationModelDto(CamelModel):
    """
    Модель данных для создания новой организации.
    """

    title: str
    token: UUID


class UpdateOrganizationModelDto(CamelModel):
    """
    Модель данных для обновления информации об организации.
    """

    title: str
