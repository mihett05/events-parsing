import pytest

from application.users.usecases import ReadAllUsersUseCase
from domain.users.dtos import ReadAllUsersDto
from domain.users.entities import User


@pytest.mark.asyncio
async def test_read_all_one_user(
    read_all_users_usecase: ReadAllUsersUseCase,
    read_all_users_dto: ReadAllUsersDto,
    create_user: User,
):
    users = await read_all_users_usecase(read_all_users_dto)

    assert len(users) == 1
    assert users[0] == create_user


@pytest.mark.asyncio
async def test_read_all_empty(
    read_all_users_usecase: ReadAllUsersUseCase,
    read_all_users_dto: ReadAllUsersDto,
):
    read_all_users_dto.page = 10
    users = await read_all_users_usecase(read_all_users_dto)

    assert len(users) == 0


@pytest.mark.asyncio
async def test_read_all_many_user(
    read_all_users_usecase: ReadAllUsersUseCase,
    read_all_users_dto: ReadAllUsersDto,
    create_users: list[User],
):
    users = await read_all_users_usecase(read_all_users_dto)

    assert len(users) <= read_all_users_dto.page_size

    attrs = ("fullname", "email", "id")
    for i in range(min(len(users), read_all_users_dto.page_size)):
        for attr in attrs:
            assert getattr(users[i], attr) == getattr(create_users[i], attr)

