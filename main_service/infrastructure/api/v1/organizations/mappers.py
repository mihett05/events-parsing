from adaptix import P
from adaptix.conversion import link_function
from application.organizations.dtos import UpdateOrganizationDto
from domain.organizations.dtos import CreateOrganizationDto
from domain.organizations.entities import Organization, OrganizationToken
from domain.users.entities import User

from infrastructure.api.retort import pydantic_retort

from .dtos import (
    CreateOrganizationModelDto,
    UpdateOrganizationModelDto,
)
from .models import OrganizationModel, OrganizationTokenModel

retort = pydantic_retort.extend(recipe=[])


@retort.impl_converter(
    recipe=[
        link_function(
            lambda model, user: user.id,
            P[CreateOrganizationDto].owner_id,
        ),
    ]
)
def map_create_dto_from_pydantic(
    model: CreateOrganizationModelDto,
    user: User,  # noqa
) -> CreateOrganizationDto: ...


"""Конвертер для преобразования модели создания организации API в DTO доменного слоя.
Добавляет ID владельца организации на основе текущего пользователя.
"""


map_to_pydantic = retort.get_converter(
    Organization,
    OrganizationModel,
    recipe=[
        link_function(
            lambda organization: organization.id,
            P[OrganizationModel].id,
        ),
        link_function(
            lambda organization: organization.created_at,
            P[OrganizationModel].created_at,
        ),
    ],
)
"""Конвертер для преобразования сущности организации в модель API."""


@retort.impl_converter(
    recipe=[
        link_function(
            lambda dto, organization_id: organization_id,
            P[UpdateOrganizationDto].id,
        ),
    ]
)
def map_update_dto_from_pydantic(
    dto: UpdateOrganizationModelDto,
    organization_id: int,  # noqa
) -> UpdateOrganizationDto: ...


"""Конвертер для преобразования модели обновления организации API в DTO прикладного слоя.
Добавляет ID организации для идентификации обновляемой записи.
"""


organization_token_map_to_pydantic = retort.get_converter(
    OrganizationToken,
    OrganizationTokenModel,
)
"""Конвертер для преобразования сущности токена организации в модель API."""
