import pytest
from openai import organization

from application.users.usecases import CreateUserRoleUseCase
from domain.users.entities import UserOrganizationRole
from domain.users.enums import RoleEnum


@pytest.mark.asyncio
async def test_create_success(
    create_user_role_usecase: CreateUserRoleUseCase,
    get_user_role_entity: UserOrganizationRole,
):
    role = await create_user_role_usecase(get_user_role_entity)
    assert role.organization_id == 1
    assert role.user_id == 1
    assert role.role == RoleEnum.SUPER_OWNER
