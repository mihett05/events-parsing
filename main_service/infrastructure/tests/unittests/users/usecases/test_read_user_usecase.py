import pytest
from application.users.usecases import ReadUserUseCase
from domain.users.entities import User
from domain.users.exceptions import UserNotFoundError


@pytest.mark.asyncio
async def test_read_success(read_user_usecase: ReadUserUseCase, create_user):
    user_create = await create_user()
    user = await read_user_usecase(user_create.id)
    assert user == user_create


@pytest.mark.asyncio
async def test_read_not_found(read_user_usecase: ReadUserUseCase):
    with pytest.raises(UserNotFoundError):
        await read_user_usecase(404)
