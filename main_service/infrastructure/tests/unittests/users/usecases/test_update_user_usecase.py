from copy import copy

import pytest
from application.users.dtos import UpdateUserDto
from application.users.usecases import UpdateUserUseCase
from domain.users.entities import User
from domain.users.exceptions import UserNotFoundError


@pytest.mark.asyncio
async def test_update_success(update_user_usecase: UpdateUserUseCase, update_user_dto):
    create_user, dto = update_user_dto
    create_user = copy(create_user)
    user = await update_user_usecase(dto, create_user)

    assert user.fullname != create_user.fullname

    assert user.fullname == dto.fullname


@pytest.mark.asyncio
async def test_update_not_found(
    update_user_usecase: UpdateUserUseCase,
    update_user_dto: UpdateUserDto,
):
    create_user, dto = update_user_dto
    dto.user_id = 404
    with pytest.raises(UserNotFoundError):
        await update_user_usecase(dto, create_user)
