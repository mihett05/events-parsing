from copy import copy

import pytest
from application.users.usecases import ReadUserRoleUseCase, UpdateUserRoleUseCase
from domain.organizations.entities import Organization
from domain.users.entities import User, UserOrganizationRole
from domain.users.exceptions import UserRoleNotFoundError


@pytest.mark.asyncio
async def test_update_success(
    update_user_role_usecase: UpdateUserRoleUseCase,
    update_user_role_dto: UserOrganizationRole,
    init_entities: tuple[User, Organization, UserOrganizationRole],
    get_admin_role: UserOrganizationRole, # noqa
    read_user_role_usecase: ReadUserRoleUseCase,
):
    admin, *_ = init_entities

    old_role = await read_user_role_usecase(
        update_user_role_dto.user_id, update_user_role_dto.organization_id
    )
    new_role = await update_user_role_usecase(update_user_role_dto, admin)

    assert new_role.role != old_role.role
    assert new_role.role == update_user_role_dto.role


@pytest.mark.asyncio
async def test_update_not_found(
    update_user_role_usecase: UpdateUserRoleUseCase,
    update_user_role_dto: UserOrganizationRole,
    get_admin: User,
    get_admin_role: UserOrganizationRole, # noqa
):
    update_user_role_dto.user_id = 404
    with pytest.raises(UserRoleNotFoundError):
        await update_user_role_usecase(update_user_role_dto, get_admin)
