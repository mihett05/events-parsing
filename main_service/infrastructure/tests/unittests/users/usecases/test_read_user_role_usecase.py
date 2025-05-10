import pytest

from application.users.usecases import ReadUserRoleUseCase
from domain.users.entities import UserOrganizationRole
from domain.users.exceptions import UserRoleNotFoundError


@pytest.mark.asyncio
async def test_read_success(
    read_user_role_usecase: ReadUserRoleUseCase,
    create_user_role: UserOrganizationRole,
):
    role = await read_user_role_usecase(create_user_role.user_id, create_user_role.organization_id)
    assert role == create_user_role


@pytest.mark.asyncio
async def test_read_not_found(read_user_role_usecase: ReadUserRoleUseCase):
    with pytest.raises(UserRoleNotFoundError):
        await read_user_role_usecase(404, 89194985188)
