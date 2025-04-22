import pytest
from application.users.usecases import ReadUserUseCase
from domain.users.entities import User
from domain.users.exceptions import UserNotFoundError


@pytest.mark.asyncio
async def test_read_success(
    read_user_usecase: ReadUserUseCase,
    create_user: User,
):
    user = await read_user_usecase(create_user.id)
    assert user == create_user


@pytest.mark.asyncio
async def test_read_not_found(read_user_usecase: ReadUserUseCase):
    with pytest.raises(UserNotFoundError):
        await read_user_usecase(404)