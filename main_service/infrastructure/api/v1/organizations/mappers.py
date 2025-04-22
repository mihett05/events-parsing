from adaptix import P
from adaptix.conversion import link_function

from infrastructure.api.retort import pydantic_retort
from main_service.application.organizations.dtos import UpdateOrganizationDto
from main_service.domain.organizations.dtos import CreateOrganizationDto
from main_service.domain.organizations.entities import Organization

from .dtos import (
    CreateOrganizationModelDto,
    UpdateOrganizationModelDto,
)
from .models import OrganizationModel

retort = pydantic_retort.extend(recipe=[])

map_create_dto_from_pydantic = retort.get_converter(
    CreateOrganizationModelDto, CreateOrganizationDto
)


@retort.impl_converter(
    recipe=[
        link_function(
            lambda organization: organization.id,
            P[OrganizationModel].id,
        ),
        link_function(
            lambda organization: organization.created_at,
            P[OrganizationModel].created_at,
        ),
    ]
)
def map_to_pydantic(organization: Organization) -> OrganizationModel: ...


@retort.impl_converter(
    recipe=[
        link_function(
            lambda dto, organization_id: organization_id,
            P[UpdateOrganizationDto].organization_id,
        )
    ]
)
def map_update_dto_from_pydantic(
    dto: UpdateOrganizationModelDto, organization_id: int
) -> UpdateOrganizationDto: ...
