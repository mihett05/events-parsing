from copy import copy

import pytest
from application.users.dtos import UpdateUserDto
from application.users.usecases import UpdateUserUseCase
from domain.users.entities import User
from domain.users.exceptions import UserNotFoundError


@pytest.mark.asyncio
async def test_update_success(
    update_user_usecase: UpdateUserUseCase,
    get_admin: User,
    get_user_entity: User,
    update_user_dto: UpdateUserDto,
):
    old_user = copy(get_user_entity)
    user = await update_user_usecase(update_user_dto, get_user_entity)

    assert user.fullname == update_user_dto.fullname
    assert user.fullname != old_user.fullname


@pytest.mark.asyncio
async def test_update_not_found(
    update_user_usecase: UpdateUserUseCase,
    get_admin: User,
    update_user_dto: UpdateUserDto,
):
    update_user_dto.user_id = 404
    with pytest.raises(UserNotFoundError):
        await update_user_usecase(update_user_dto, get_admin)
