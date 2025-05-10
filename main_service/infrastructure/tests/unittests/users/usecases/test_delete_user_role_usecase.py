import pytest

from application.users.dtos import DeleteUserRoleDto
from application.users.usecases import DeleteUserRoleUseCase, ReadUserRoleUseCase
from domain.users.entities import UserOrganizationRole
from domain.users.exceptions import UserRoleNotFoundError


@pytest.mark.asyncio
async def delete_user_success(
    read_user_role_usecase: ReadUserRoleUseCase,
    delete_user_role_usecase: DeleteUserRoleUseCase,
    delete_user_role_dto: DeleteUserRoleDto,
):
    role = await read_user_role_usecase(delete_user_role_dto.user_id, delete_user_role_dto.organization_id)
    deleted_role = await delete_user_role_usecase(delete_user_role_dto)
    assert deleted_role == role

    with pytest.raises(UserRoleNotFoundError):
        await read_user_role_usecase(delete_user_role_dto.user_id, delete_user_role_dto.organization_id)


@pytest.mark.asyncio
async def test_delete_not_found(
    delete_user_role_usecase: DeleteUserRoleUseCase, create_user_role: UserOrganizationRole
):
    await delete_user_role_usecase(create_user_role)
    with pytest.raises(UserRoleNotFoundError):
        await delete_user_role_usecase(create_user_role)
