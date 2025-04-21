from adaptix import P
from adaptix.conversion import (
    allow_unlinked_optional,
    link_function,
)

from domain.organizations.dtos import CreateOrganizationDto
from domain.organizations.entities import Organization
from infrastructure.database.mappers import postgres_retort

from .models import OrganizationDatabaseModel

retort = postgres_retort.extend(recipe=[])

map_from_db = retort.get_converter(
    OrganizationDatabaseModel,
    Organization,
)


@retort.impl_converter(
    recipe=[
        link_function(
            lambda event: event.id,
            P[OrganizationDatabaseModel].id,
        ),
        link_function(
            lambda event: event.created_at,
            P[OrganizationDatabaseModel].created_at,
        ),
    ]
)
def map_to_db(organization: Organization) -> OrganizationDatabaseModel: ...


@retort.impl_converter(
    recipe=[
        allow_unlinked_optional(P[OrganizationDatabaseModel].id),
        allow_unlinked_optional(P[OrganizationDatabaseModel].created_at),
    ]
)

def map_create_dto_to_model(dto: CreateOrganizationDto) -> OrganizationDatabaseModel: ...