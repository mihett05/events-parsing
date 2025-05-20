from adaptix import P
from adaptix.conversion import allow_unlinked_optional, coercer, link_function
from domain.users.dtos import CreateTelegramTokenDto
from domain.users.entities import (
    TelegramToken,
    User,

from adaptix._internal.conversion.facade.provider import allow_unlinked_optional
from adaptix.conversion import coercer, link_function
from domain.users.dtos import CreateActivationTokenDto
from domain.users.entities import (
    User,
    UserActivationToken,
    UserOrganizationRole,
    UserSettings,
)

from ...mappers import postgres_retort
from .models import (
    TelegramTokenDatabaseModel,
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

user_settings_to_db_mapper = retort.get_converter(
    UserSettings,
    UserSettingsDatabaseModel,
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
        coercer(
            UserSettingsDatabaseModel,
            UserSettings,
            user_settings_to_db_mapper,
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

telegram_token_map_to_db = retort.get_converter(
    TelegramToken,
    TelegramTokenDatabaseModel,
    recipe=[
        link_function(
            lambda token: token.created_at, P[TelegramTokenDatabaseModel].created_at
        ),
    ],
)

telegram_token_map_from_db = retort.get_converter(
    TelegramTokenDatabaseModel, TelegramToken
)

telegram_token_map_create_to_model = retort.get_converter(
    CreateTelegramTokenDto,
    TelegramTokenDatabaseModel,
    recipe=[
        allow_unlinked_optional(P[TelegramTokenDatabaseModel].created_at),
        allow_unlinked_optional(P[TelegramTokenDatabaseModel].is_used),

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

create_user_activation_token_map = retort.get_converter(
    CreateActivationTokenDto,
    UserActivationTokenDatabaseModel,
    recipe=[
        coercer(User, UserDatabaseModel, map_to_db),
        allow_unlinked_optional(P[UserActivationTokenDatabaseModel].id),
        allow_unlinked_optional(P[UserActivationTokenDatabaseModel].is_used),
    ],
)
