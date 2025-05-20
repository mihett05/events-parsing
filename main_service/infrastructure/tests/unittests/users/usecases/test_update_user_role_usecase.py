from copy import copy

import pytest
from application.users.usecases import UpdateUserRoleUseCase
from domain.users.entities import User, UserOrganizationRole
from domain.users.exceptions import UserRoleNotFoundError


@pytest.mark.asyncio
async def test_update_success(
    update_user_role_usecase: UpdateUserRoleUseCase,
    update_user_role_entity: UserOrganizationRole,
    create_user_role: UserOrganizationRole,
    get_actor: User,
):
    create_user = copy(create_user_role)
    user = await update_user_role_usecase(update_user_role_entity, get_actor)

    assert user.role != create_user.role

    assert user.role == update_user_role_entity.role


@pytest.mark.asyncio
async def test_update_not_found(
    update_user_role_usecase: UpdateUserRoleUseCase,
    update_user_role_entity: UserOrganizationRole,
    get_actor: User,
):
    update_user_role_entity.user_id = 404
    with pytest.raises(UserRoleNotFoundError):
        await update_user_role_usecase(update_user_role_entity, get_actor)
