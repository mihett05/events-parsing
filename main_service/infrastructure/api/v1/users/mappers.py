from adaptix import P
from adaptix.conversion import link_function
from application.users.dtos import UpdateUserDto, DeleteUserRoleDto
from domain.users.entities import User, UserOrganizationRole

from infrastructure.api.retort import pydantic_retort
from infrastructure.mocks.repositories.mails.mappers import (
    map_create_dto_to_entity,
)

from .dtos import (
    CreateUserRoleModelDto,
    UpdateUserModelDto,
    UpdateUserRoleModelDto,
)
from .models import UserModel, UserRoleModel

retort = pydantic_retort.extend(recipe=[])

map_to_pydantic = retort.get_converter(
    User,
    UserModel,
    recipe=[
        link_function(
            lambda user: user.id,
            P[UserModel].id,
        )
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
    dto: UpdateUserModelDto, user_id: int
) -> UpdateUserDto: ...


map_role_to_pydantic = retort.get_converter(UserOrganizationRole, UserRoleModel)

map_create_role_dto_to_entity = retort.get_converter(
    CreateUserRoleModelDto, UserOrganizationRole
)


map_update_role_entity_from_pydantic = retort.get_converter(
    UpdateUserRoleModelDto, UserOrganizationRole
)


def map_delete_role_to_dto(
    user_id: int, organization_id:int
) -> DeleteUserRoleDto:
    return DeleteUserRoleDto(user_id, organization_id)