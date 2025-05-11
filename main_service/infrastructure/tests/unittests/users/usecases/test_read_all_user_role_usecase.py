import pytest
from application.users.usecases import ReadUserRolesUseCase
from domain.users.entities import UserOrganizationRole


@pytest.mark.asyncio
async def test_read_success(
    read_user_roles_usecase: ReadUserRolesUseCase,
    create_user_role: UserOrganizationRole,
):
    role = await read_user_roles_usecase(create_user_role.user_id)
    assert role[0] == create_user_role
