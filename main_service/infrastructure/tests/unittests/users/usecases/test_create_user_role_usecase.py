import pytest
from application.users.usecases import CreateUserRoleUseCase
from domain.users.entities import User


@pytest.mark.asyncio
async def test_create_success(
    create_user_role_usecase: CreateUserRoleUseCase,
    create_user_role_dto,
    get_admin: User,
):
    role = await create_user_role_usecase(create_user_role_dto, get_admin)

    assert role.organization_id == create_user_role_dto.organization_id
    assert role.user_id == create_user_role_dto.user_id
    assert role.role == create_user_role_dto.role
