import pytest
import pytest_asyncio
from application.users.dtos import UpdateUserDto
from dishka import AsyncContainer
from domain.users.dtos import (
    ReadAllUsersDto,
)
from domain.users.entities import User
from domain.users.repositories import UsersRepository





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
    get_user_entity: User,
    users_repository: UsersRepository,
) -> User:
    user = await users_repository.create(get_user_entity)
    return user


@pytest_asyncio.fixture
async def create_users(
    get_user_entities: list[User],
    users_repository: UsersRepository,
) -> list[User]:
    return [
        await users_repository.create(user_entity)
        for user_entity in get_user_entities
    ]


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare(
    pytestconfig: pytest.Config, users_repository: UsersRepository
):
    yield
    if pytestconfig.getoption("--integration", default=False):
        return
    await users_repository.clear()  # noqa
