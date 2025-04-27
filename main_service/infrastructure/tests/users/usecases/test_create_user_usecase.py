import pytest
from application.users.usecases import CreateUserUseCase
from domain.users.entities import User


@pytest.mark.asyncio
async def test_create_success(
    create_user_usecase: CreateUserUseCase,
    get_user_entity: User,
):
    user = await create_user_usecase(get_user_entity)

    attrs = ("fullname", "email")
    for attr in attrs:
        assert getattr(user, attr) == getattr(get_user_entity, attr)

    assert user.id == 1
