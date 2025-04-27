import random

import pytest

from application.auth.dtos import RegisterUserDTO
from application.auth.usecases import RegisterUseCase
from application.users.usecases import DeleteUserUseCase, ReadUserUseCase
from domain.users.entities import User
from domain.users.exceptions import UserNotFoundError


@pytest.mark.asyncio
async def delete_user_success(
    read_user_usecase: ReadUserUseCase,
    delete_user_usecase: DeleteUserUseCase,
    register_user_usecase: RegisterUseCase,
    register_user_dto: RegisterUserDTO,
):
    user, _ = await register_user_usecase(dto=register_user_dto)
    deleted_user = await delete_user_usecase(user)
    assert deleted_user == user

    with pytest.raises(UserNotFoundError):
        await read_user_usecase(user.id)


@pytest.mark.asyncio
async def test_delete_not_found(
    delete_user_usecase: DeleteUserUseCase, create_user: User
):
    await delete_user_usecase(create_user)
    with pytest.raises(UserNotFoundError):
        await delete_user_usecase(create_user)
