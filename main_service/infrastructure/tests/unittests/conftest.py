from typing import Callable, Coroutine, Any

import pytest
import pytest_asyncio
from dishka import AsyncContainer
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from application.auth.dtos import RegisterUserDTO
from application.auth.usecases import RegisterUseCase
from domain.organizations.dtos import CreateOrganizationDto
from domain.organizations.entities import Organization
from domain.organizations.repositories import OrganizationsRepository
from domain.users.entities import User
from domain.users.repositories import UsersRepository
from infrastructure.database.postgres import Base
from infrastructure.tests.configs import get_container
import application.auth.usecases as auth_usecases
import application.users.usecases as user_usecases


def pytest_addoption(parser):
    parser.addoption(
        "--integration",
        action="store_true",
        help="Run tests with testcontainers",
    )


@pytest_asyncio.fixture(scope="session")
async def container(pytestconfig: pytest.Config):
    async with get_container(
        bool(pytestconfig.getoption("--integration", default=False))
    ) as container:
        try:
            yield container
        finally:
            await container.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db_tables(
    pytestconfig: pytest.Config, container: AsyncContainer
):
    if not pytestconfig.getoption("--integration", default=False):
        return
    engine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_data(pytestconfig: pytest.Config, container: AsyncContainer):
    if not pytestconfig.getoption("--integration", default=False):
        return
    engine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(
                text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE")
            )


@pytest_asyncio.fixture
async def get_user_entity() -> User:
    return User(
        email="test@example.com",
        fullname="Ivanov Ivan Ivanovich",
    )


@pytest_asyncio.fixture
async def get_user_entities() -> list[User]:
    return [
        User(
            email=f"test{i}@test.com",
            fullname=f"Ivan{i}",
        )
        for i in range(8)
    ]


@pytest_asyncio.fixture
async def create_user1(
    register_user1_dto: RegisterUserDTO,
    register_usecase: RegisterUseCase,
    users_repository: UsersRepository,
) -> Callable[..., Coroutine[Any, Any, User]]:
    async def _factory() -> User:
        user1, _ = await register_usecase(register_user1_dto)
        return user1

    return _factory

@pytest_asyncio.fixture
async def register_user1_dto() -> RegisterUserDTO:
    return RegisterUserDTO(
        email="test@example.com",
        password="12345678",
        fullname="Ivanov Ivan Ivanovich",
    )

@pytest_asyncio.fixture
async def register_usecase(
    container: AsyncContainer,
) -> auth_usecases.RegisterUseCase:
    async with container() as nested:
        yield await nested.get(auth_usecases.RegisterUseCase)

@pytest_asyncio.fixture
async def create_usecase_usecase(
    container: AsyncContainer,
) -> user_usecases.CreateUserOrganizationRoleUseCase:
    async with container() as nested:
        yield await nested.get(user_usecases.CreateUserOrganizationRoleUseCase)

@pytest_asyncio.fixture
async def create_organization(
    create_organization_dto: CreateOrganizationDto,
    organizations_repository: OrganizationsRepository,
) -> Callable[..., Coroutine[Any, Any, Organization]]:
    async def _factory():
        return await organizations_repository.create(create_organization_dto)
    return _factory

@pytest_asyncio.fixture
async def create_organization_dto() -> CreateOrganizationDto:
    return CreateOrganizationDto(
        title="Test Organization", owner_id=1, token=
    )

@pytest_asyncio.fixture
async def organizations_repository(
    container: AsyncContainer,
) -> OrganizationsRepository:
    async with container() as request_container:
        yield await request_container.get(OrganizationsRepository)