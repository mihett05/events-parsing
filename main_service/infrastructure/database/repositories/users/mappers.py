from adaptix import P
from adaptix.conversion import allow_unlinked_optional, coercer, link_function
from application.auth.dtos import CreateUserWithPasswordDto
from domain.users.dtos import (
    CreateActivationTokenDto,
    CreatePasswordResetTokenDto,
    CreateTelegramTokenDto,
)
from domain.users.entities import (
    PasswordResetToken,
    TelegramToken,
    User,
    UserActivationToken,
    UserOrganizationRole,
    UserSettings,
)

from ...mappers import postgres_retort
from .models import (
    PasswordResetTokenDatabaseModel,
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
"""
Преобразует модель настроек пользователя из базы данных в сущность домена.
"""

user_settings_to_db_mapper = retort.get_converter(
    UserSettings,
    UserSettingsDatabaseModel,
)
"""
Преобразует сущность настроек пользователя в модель базы данных.
"""

user_organization_role_map_from_db = retort.get_converter(
    UserOrganizationRoleDatabaseModel,
    UserOrganizationRole,
)
"""
Преобразует модель роли пользователя в организации из базы данных в сущность домена.
"""

user_organization_role_map_to_db = retort.get_converter(
    UserOrganizationRole,
    UserOrganizationRoleDatabaseModel,
)
"""
Преобразует сущность роли пользователя в организации в модель базы данных.
"""

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
"""
Преобразует модель пользователя из базы данных в сущность домена, включая настройки.
"""

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
            UserSettings,
            UserSettingsDatabaseModel,
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
"""
Преобразует сущность пользователя в модель базы данных, сохраняя ключевые атрибуты.
"""

create_user_mapper = retort.get_converter(
    CreateUserWithPasswordDto,
    UserDatabaseModel,
    recipe=[
        allow_unlinked_optional(P[UserDatabaseModel].id),
        allow_unlinked_optional(P[UserDatabaseModel].settings),
        allow_unlinked_optional(P[UserDatabaseModel].telegram_id),
        allow_unlinked_optional(P[UserDatabaseModel].created_at),
    ],
)
"""
Преобразует DTO создания пользователя с паролем в модель базы данных, допуская отсутствие некоторых полей.
"""


telegram_token_map_to_db = retort.get_converter(
    TelegramToken,
    TelegramTokenDatabaseModel,
    recipe=[
        link_function(
            lambda token: token.created_at,
            P[TelegramTokenDatabaseModel].created_at,
        ),
    ],
)
"""
Преобразует сущность токена Telegram в модель базы данных, сохраняя дату создания.
"""


telegram_token_map_from_db = retort.get_converter(
    TelegramTokenDatabaseModel, TelegramToken
)
"""
Преобразует модель токена Telegram из базы данных в сущность домена.
"""

telegram_token_map_create_to_model = retort.get_converter(
    CreateTelegramTokenDto,
    TelegramTokenDatabaseModel,
    recipe=[
        allow_unlinked_optional(P[TelegramTokenDatabaseModel].created_at),
        allow_unlinked_optional(P[TelegramTokenDatabaseModel].is_used),
    ],
)
"""
Преобразует DTO создания токена Telegram в модель базы данных, допуская отсутствие некоторых полей.
"""

user_activation_token_map_from_db = retort.get_converter(
    UserActivationTokenDatabaseModel,
    UserActivationToken,
    recipe=[coercer(UserDatabaseModel, User, map_from_db)],
)
"""
Преобразует модель токена активации пользователя из базы данных в сущность домена, включая связанного пользователя.
"""

user_activation_token_map_to_db = retort.get_converter(
    UserActivationToken,
    UserActivationTokenDatabaseModel,
    recipe=[coercer(User, UserDatabaseModel, map_to_db)],
)
"""
Преобразует сущность токена активации пользователя в модель базы данных, включая связанного пользователя.
"""

create_user_activation_token_map = retort.get_converter(
    CreateActivationTokenDto,
    UserActivationTokenDatabaseModel,
    recipe=[
        coercer(User, UserDatabaseModel, map_to_db),
        allow_unlinked_optional(P[UserActivationTokenDatabaseModel].id),
        allow_unlinked_optional(P[UserActivationTokenDatabaseModel].is_used),
    ],
)
"""
Преобразует DTO создания токена активации пользователя в модель базы данных, допуская отсутствие некоторых полей.
"""

password_reset_token_map_from_db = retort.get_converter(
    PasswordResetTokenDatabaseModel,
    PasswordResetToken,
    recipe=[coercer(UserDatabaseModel, User, map_from_db)],
)

password_reset_token_map_to_db = retort.get_converter(
    PasswordResetToken,
    PasswordResetTokenDatabaseModel,
    recipe=[coercer(User, UserDatabaseModel, map_to_db)],
)

create_password_reset_token_map = retort.get_converter(
    CreatePasswordResetTokenDto,
    PasswordResetTokenDatabaseModel,
    recipe=[
        coercer(User, UserDatabaseModel, map_to_db),
        allow_unlinked_optional(P[PasswordResetTokenDatabaseModel].id),
        allow_unlinked_optional(P[PasswordResetTokenDatabaseModel].is_used),
    ],
)
