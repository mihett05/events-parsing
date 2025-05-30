from adaptix import P
from adaptix.conversion import allow_unlinked_optional, link_function
from domain.organizations.dtos import (
    CreateOrganizationDto,
    CreateOrganizationTokenDto,
)
from domain.organizations.entities import Organization, OrganizationToken

from infrastructure.database.mappers import postgres_retort

from .models import OrganizationDatabaseModel, OrganizationTokenDatabaseModel

retort = postgres_retort.extend(recipe=[])

map_from_db = retort.get_converter(
    OrganizationDatabaseModel,
    Organization,
)

map_to_db = retort.get_converter(
    Organization,
    OrganizationDatabaseModel,
    recipe=[
        link_function(
            lambda organization: organization.id,
            P[OrganizationDatabaseModel].id,
        ),
        link_function(
            lambda organization: organization.created_at,
            P[OrganizationDatabaseModel].created_at,
        ),
    ],
)

map_create_dto_to_model = retort.get_converter(
    CreateOrganizationDto,
    OrganizationDatabaseModel,
    recipe=[
        allow_unlinked_optional(P[OrganizationDatabaseModel].id),
        allow_unlinked_optional(P[OrganizationDatabaseModel].created_at),
    ],
)

organization_token_map_to_db = retort.get_converter(
    OrganizationToken,
    OrganizationTokenDatabaseModel,
)

organization_token_map_from_db = retort.get_converter(
    OrganizationTokenDatabaseModel,
    OrganizationToken,
)

organization_token_map_create_to_model = retort.get_converter(
    CreateOrganizationTokenDto,
    OrganizationTokenDatabaseModel,
    recipe=[
        allow_unlinked_optional(P[OrganizationTokenDatabaseModel].used_by),
        allow_unlinked_optional(P[OrganizationTokenDatabaseModel].is_used),
    ],
)
