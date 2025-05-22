import pytest
from application.users.usecases import CreateUserRoleUseCase
from domain.users.entities import User


@pytest.mark.asyncio
async def test_create_success(
    create_user_role_usecase: CreateUserRoleUseCase,
    get_user_role_entity,
    get_actor: User,
):
    role = await create_user_role_usecase(get_user_role_entity, get_actor)
    assert role.organization_id == 1
    assert role.user_id == get_user_role_entity.user_id
    assert role.role == get_user_role_entity.role
