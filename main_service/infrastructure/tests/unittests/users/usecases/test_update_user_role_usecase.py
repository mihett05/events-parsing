from copy import copy

import pytest

from application.users.usecases import UpdateUserRoleUseCase
from domain.users.entities import UserOrganizationRole
from domain.users.exceptions import UserRoleNotFoundError


@pytest.mark.asyncio
async def test_update_success(
    update_user_role_usecase: UpdateUserRoleUseCase,
    update_user_role_entity: UserOrganizationRole,
    create_user_role: UserOrganizationRole,
):
    create_user = copy(create_user_role)
    user = await update_user_usecase(update_user_role_entity, None)

    assert user.role != create_user.role

    assert user.role == update_user_role_entity.role


@pytest.mark.asyncio
async def test_update_not_found(
    update_user_role_usecase: UpdateUserRoleUseCase,
    update_user_role_entity: UserOrganizationRole,
):
    update_user_role_entity = 404
    with pytest.raises(UserRoleNotFoundError):
        await update_user_usecase(update_user_role_entity, None)
