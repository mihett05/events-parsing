from adaptix import P
from adaptix.conversion import coercer, link_function
from domain.users.entities import (
    User,
    UserActivationToken,
    UserOrganizationRole,
    UserSettings,
)

from ...mappers import postgres_retort
from .models import (
    UserActivationTokenDatabaseModel,
    UserDatabaseModel,
    UserOrganizationRoleDatabaseModel,
    UserSettingsDatabaseModel,
)

retort = postgres_retort.extend(recipe=[])

user_settings_from_db_mapper = retort.get_converter(
    UserSettingsDatabaseModel,
    UserSettings,
)

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
    recipe=[
        coercer(
            UserSettingsDatabaseModel,
            UserSettings,
            user_settings_from_db_mapper,
        )
    ],
)

map_to_db = retort.get_converter(
    User,
    UserDatabaseModel,
    recipe=[
        link_function(
            lambda user: user.id,
            P[UserDatabaseModel].id,
        ),
        link_function(
            lambda user: user.salt,
            P[UserDatabaseModel].salt,
        ),
        link_function(
            lambda user: user.settings,
            P[UserDatabaseModel].settings,
        ),
        link_function(
            lambda user: user.created_at,
            P[UserDatabaseModel].created_at,
        ),
        link_function(
            lambda user: user.hashed_password,
            P[UserDatabaseModel].hashed_password,
        ),
    ],
)

user_activation_token_map_from_db = retort.get_converter(
    UserActivationTokenDatabaseModel,
    UserActivationToken,
    recipe=[coercer(UserDatabaseModel, User, map_from_db)],
)

user_activation_token_map_to_db = retort.get_converter(
    UserActivationToken,
    UserActivationTokenDatabaseModel,
    recipe=[coercer(User, UserDatabaseModel, map_to_db)],
)
