from adaptix import P
from adaptix.conversion import link_function

from application.organizations.dtos import UpdateOrganizationDto
from domain.organizations.dtos import CreateOrganizationDto
from domain.organizations.entities import Organization
from domain.users.entities import User
from infrastructure.api.retort import pydantic_retort

from .dtos import (
    CreateOrganizationModelDto,
    UpdateOrganizationModelDto,
)
from .models import OrganizationModel

retort = pydantic_retort.extend(recipe=[])


@retort.impl_converter(
    recipe=[
        link_function(
            lambda model, user: model.created_at,
            P[CreateOrganizationDto].created_at,
        ),
        link_function(
            lambda model, user: user.id,
            P[CreateOrganizationDto].owner_id,
        ),
    ]
)
def map_create_dto_from_pydantic(
    model: CreateOrganizationModelDto, user: User
) -> CreateOrganizationDto: ...


map_to_pydantic = retort.get_converter(
    Organization,
    OrganizationModel,
    recipe=[
        link_function(
            lambda organization: organization.id,
            P[OrganizationModel].id,
        )
    ],
)


@retort.impl_converter(
    recipe=[
        link_function(
            lambda dto, organization_id: organization_id,
            P[UpdateOrganizationDto].id,
        ),
    ]
)
def map_update_dto_from_pydantic(
    dto: UpdateOrganizationModelDto, organization_id: int
) -> UpdateOrganizationDto: ...
