from adaptix import P
from adaptix.conversion import allow_unlinked_optional, link_function
from domain.users.entities import User, UserOrganizationRole

from infrastructure.database.mappers import postgres_retort

from .models import UserDatabaseModel, UserOrganizationRoleDatabaseModel

retort = postgres_retort.extend(recipe=[])

user_organization_role_map_from_db = retort.get_converter(
    UserOrganizationRoleDatabaseModel,
    UserOrganizationRole,
)

user_organization_role_map_to_db = retort.get_converter(
    UserOrganizationRole,
    UserOrganizationRoleDatabaseModel,
)

map_from_db = retort.get_converter(
    UserDatabaseModel,
    User,
)

map_to_db = retort.get_converter(
    User,
    UserDatabaseModel,
    recipe=[
        allow_unlinked_optional(P[User].salt),
        allow_unlinked_optional(P[User].created_at),
        allow_unlinked_optional(P[User].hashed_password),
        link_function(
            lambda user: user.id,
            P[UserDatabaseModel].id,
        ),
    ],
)
