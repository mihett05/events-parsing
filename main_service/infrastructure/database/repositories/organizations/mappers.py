from adaptix import P
from adaptix.conversion import allow_unlinked_optional, link_function

from domain.organizations.dtos import CreateOrganizationDto
from domain.organizations.entities import Organization
from infrastructure.database.mappers import postgres_retort

from .models import OrganizationDatabaseModel

retort = postgres_retort.extend(recipe=[])

map_from_db = retort.get_converter(
    OrganizationDatabaseModel,
    Organization,
    recipe=[
        link_function(
            lambda organization: organization.id,
            P[Organization].id,
        )
    ]
)

map_to_db = retort.get_converter(
    Organization,
    OrganizationDatabaseModel,
)

map_create_dto_to_model = retort.get_converter(
    CreateOrganizationDto,
    OrganizationDatabaseModel,
    recipe=[
        allow_unlinked_optional(P[OrganizationDatabaseModel].id),
        allow_unlinked_optional(P[OrganizationDatabaseModel].created_at),
        allow_unlinked_optional(P[OrganizationDatabaseModel].title),
    ]
)