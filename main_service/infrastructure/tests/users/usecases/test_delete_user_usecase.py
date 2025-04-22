import random

import pytest
from application.users.usecases import DeleteUserUseCase, ReadUserUseCase
from domain.users.entities import User
from domain.users.exceptions import UserNotFoundError


@pytest.mark.asyncio
async def user_delete_success(
    read_user_usecase: ReadUserUseCase,
    delete_user_usecase: DeleteUserUseCase,
    create_user: User,
):
    user = await delete_user_usecase(create_user)
    assert user == create_user

    with pytest.raises(UserNotFoundError):
        await read_user_usecase(user.id)


@pytest.mark.asyncio
async def test_delete_not_found(
    delete_user_usecase: DeleteUserUseCase,
    user: User
):
    with pytest.raises(UserNotFoundError):
        await delete_user_usecase(user)