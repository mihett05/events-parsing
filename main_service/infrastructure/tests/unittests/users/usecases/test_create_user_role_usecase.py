import pytest
from application.users.usecases import CreateUserRoleUseCase, CreateUserRoleUseCase
from domain.users.entities import User, UserOrganizationRole
from domain.users.enums import RoleEnum


@pytest.mark.asyncio
async def test_create_success(
    create_user_role_usecase: CreateUserRoleUseCase,
    get_user_role_entity: UserOrganizationRole,
    get_actor: User,
):
    role = await create_user_role_usecase(get_user_role_entity, get_actor)
    assert role.organization_id == 1
    assert role.user_id == 1
    assert role.role == RoleEnum.SUPER_OWNER
