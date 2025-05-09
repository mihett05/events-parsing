from adaptix import P
from adaptix.conversion import coercer, link_function
from application.users.dtos import UpdateUserDto
from domain.users.entities import User, UserSettings

from infrastructure.api.retort import pydantic_retort

from .dtos import (
    UpdateUserModelDto,
)
from .models import UserModel, UserSettingsModel

retort = pydantic_retort.extend(recipe=[])

map_user_settings_to_pydantic = retort.get_converter(
    UserSettings,
    UserSettingsModel,
)

map_to_pydantic = retort.get_converter(
    User,
    UserModel,
    recipe=[
        link_function(
            lambda user: user.id,
            P[UserModel].id,
        ),
        coercer(UserSettings, UserSettingsModel, map_user_settings_to_pydantic),
    ],
)


@retort.impl_converter(
    recipe=[
        link_function(
            lambda dto, user_id: user_id,
            P[UpdateUserDto].user_id,
        )
    ]
)
def map_update_dto_from_pydantic(
    dto: UpdateUserModelDto,
    user_id: int,  # noqa
) -> UpdateUserDto: ...
