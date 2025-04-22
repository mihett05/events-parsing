import pytest

from application.users.usecases import CreateUserUseCase
from domain.users.entities import User


@pytest.mark.asyncio
async def test_create_success(
    create_user_usecase: CreateUserUseCase,
    create_user: User,
):
    user = create_user
    created_user = await create_user_usecase(user)

    attrs = (
        'email',
        'fullname',
        'id',
        'is_active',
        'salt',
        'hashed_password',
        'telegram_id',
        'created_at'
    )
    for attr in attrs:
        assert getattr(user, attr) == getattr(created_user, attr)
