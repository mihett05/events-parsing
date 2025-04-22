from datetime import datetime, timedelta

import pytest_asyncio
from application.users.dtos import UpdateUserDto
from dishka import AsyncContainer
from domain.users.dtos import (
    ReadAllUsersDto,

)
from application.auth.dtos import RegisterUserDTO
from domain.users.entities import User
from domain.users.repositories import UsersRepository

@pytest_asyncio.fixture
async def create_user() -> User:
    new_user = User()
    new_user.email = 'test@test.com'
    new_user.fullname = 'Ivanov Ivan Ivanovich'
    new_user.id = 1

    return new_user


@pytest_asyncio.fixture
async def update_user_dto() -> UpdateUserDto:
    return UpdateUserDto(
        user_id=1,
        fullname="Romanov Roman Romanovich",
    )


@pytest_asyncio.fixture
async def read_all_users_dto() -> ReadAllUsersDto:
    return ReadAllUsersDto(
        page=1,
        page_size=1
    )



@pytest_asyncio.fixture
async def users_repository(container: AsyncContainer) -> UsersRepository:
    yield await container.get(UsersRepository)


@pytest_asyncio.fixture
async def create_event(
    create_user_dto: RegisterUserDTO,
    events_repository: UsersRepository,
) -> User:
    return await events_repository.create(create_user_dto)