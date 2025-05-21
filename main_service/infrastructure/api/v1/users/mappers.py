from adaptix import P
from adaptix.conversion import coercer, link_function
from application.users.dtos import DeleteUserRoleDto, UpdateUserDto
from domain.users.entities import User, UserOrganizationRole, UserSettings

from infrastructure.api.retort import pydantic_retort

from .dtos import (
    CreateUserRoleModelDto,
    UpdateUserModelDto,
    UpdateUserRoleModelDto,
)
from .models import UserModel, UserRoleModel, UserSettingsModel

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



map_role_to_pydantic = retort.get_converter(UserOrganizationRole, UserRoleModel)

map_create_role_dto_to_entity = retort.get_converter(
    CreateUserRoleModelDto, UserOrganizationRole
)


map_update_role_entity_from_pydantic = retort.get_converter(
    UpdateUserRoleModelDto, UserOrganizationRole
)


def map_delete_role_to_dto(user_id: int, organization_id: int) -> DeleteUserRoleDto:
    return DeleteUserRoleDto(user_id, organization_id)
