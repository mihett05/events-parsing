import pytest_asyncio
from dishka import AsyncContainer

from application.auth.dtos import RegisterUserDTO
from application.auth.usecases import RegisterUseCase
from application.users.dtos import UpdateUserDto
from domain.users.dtos import (
    ReadAllUsersDto,
)
from domain.users.entities import User
from domain.users.repositories import UsersRepository


@pytest_asyncio.fixture
async def register_user_dto() -> RegisterUserDTO:
    return RegisterUserDTO(
        email="test@test.com",
        password="12345678",
        fullname="Ivanov Ivan Ivanovich",
    )


@pytest_asyncio.fixture
async def register_user_dtos() -> list[RegisterUserDTO]:
    dto_list = list()
    for i in range(8):
        dto_list.append(
            RegisterUserDTO(
                email=f"test{i}@test.com",
                password=f"{i}" * 8,
                fullname=f"Iivan{i}",
            )
        )
    return dto_list


@pytest_asyncio.fixture
async def update_user_dto() -> UpdateUserDto:
    return UpdateUserDto(
        user_id=1,
        fullname="Romanov Roman Romanovich",
    )


@pytest_asyncio.fixture
async def read_all_users_dto() -> ReadAllUsersDto:
    return ReadAllUsersDto(page=0, page_size=8)


@pytest_asyncio.fixture
async def users_repository(container: AsyncContainer) -> UsersRepository:
    async with container() as nested:
        yield await nested.get(UsersRepository)


@pytest_asyncio.fixture
async def create_user(
    register_user_dto: RegisterUserDTO,
    register_user_usecase: RegisterUseCase,
    users_repository: UsersRepository,
) -> User:
    user, _ = await register_user_usecase(register_user_dto)
    return user


@pytest_asyncio.fixture
async def create_users(
    register_user_dtos: list[RegisterUserDTO],
    register_user_usecase: RegisterUseCase,
    users_repository: UsersRepository,
) -> list[User]:
    users = list()
    for dto in register_user_dtos:
        user, _ = await register_user_usecase(dto)
        users.append(user)
    return users
