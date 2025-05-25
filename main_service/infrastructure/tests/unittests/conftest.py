from typing import Any, Callable, Coroutine
from uuid import uuid4

import application.auth.usecases as auth_usecases
import application.users.usecases as user_usecases
import pytest
import pytest_asyncio
from application.auth.dtos import RegisterUserDto
from application.auth.usecases import RegisterUseCase
from dishka import AsyncContainer

from application.users.usecases import CreateUserRoleUseCase
from domain.organizations.dtos import CreateOrganizationDto
from domain.organizations.entities import Organization
from domain.organizations.repositories import OrganizationsRepository
from domain.users.entities import User, UserOrganizationRole
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from domain.users.enums import RoleEnum
from domain.users.repositories import UserOrganizationRolesRepository
from infrastructure.database.postgres import Base
from infrastructure.tests.configs import get_container


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
async def setup_db_tables(pytestconfig: pytest.Config, container: AsyncContainer):
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
        email="taaaaaa@example.com",
        fullname="Ivanov Ivan Ivanovich",
        salt="morskaya_sol",
        hashed_password="parol",
    )


@pytest_asyncio.fixture
async def get_user_entities() -> list[User]:
    return [
        User(
            email=f"test{i}@test.com",
            fullname=f"Ivan{i}",
            salt="morskaya_sol",
            hashed_password="parol",
        )
        for i in range(8)
    ]


@pytest_asyncio.fixture
async def create_user1(
    register_user1_dto: RegisterUserDto,
    register_usecase: RegisterUseCase,
) -> Callable[..., Coroutine[Any, Any, User]]:
    async def _factory() -> User:
        token1 = await register_usecase(register_user1_dto)
        return token1.user

    return _factory

@pytest_asyncio.fixture
async def create_user_role_usecase(
    container: AsyncContainer,
) -> user_usecases.CreateUserRoleUseCase:
    async with container() as nested:
        yield await nested.get(user_usecases.CreateUserRoleUseCase)

@pytest_asyncio.fixture
async def create_super_user1(
    register_user1_dto: RegisterUserDto,
    register_usecase: RegisterUseCase,
    user_organization_roles_repository: UserOrganizationRolesRepository,
    create_user1,
    create_organization,
    create_user_role_usecase
) :
    async def _factory() -> User:
        user = await create_user1()
        org = await create_organization()
        await user_organization_roles_repository.create(UserOrganizationRole(user_id= user.id, organization_id= org.id, role= RoleEnum.SUPER_USER))
        return user
    return _factory

@pytest_asyncio.fixture
async def register_user1_dto() -> RegisterUserDto:
    return RegisterUserDto(
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
) -> user_usecases.CreateUserRoleUseCase:
    async with container() as nested:
        yield await nested.get(user_usecases.CreateUserRoleUseCase)


@pytest_asyncio.fixture
async def create_organization(
    create_organization_dto: CreateOrganizationDto,
    organizations_repository: OrganizationsRepository,
) -> Callable[..., Coroutine[Any, Any, Organization]]:
    async def _factory():
        return await organizations_repository.create(create_organization_dto)

    return _factory


@pytest_asyncio.fixture
async def create_organization_dto(create_user1) -> CreateOrganizationDto:
    user = await create_user1()
    return CreateOrganizationDto(
        title="Test Organization",
        owner_id=user.id,
        token=uuid4()
    )


@pytest_asyncio.fixture
async def organizations_repository(
    container: AsyncContainer,
) -> OrganizationsRepository:
    async with container() as request_container:
        yield await request_container.get(OrganizationsRepository)

@pytest_asyncio.fixture
async def user_organization_roles_repository(
    container: AsyncContainer,
) -> UserOrganizationRolesRepository:
    async with container() as request_container:
        yield await request_container.get(UserOrganizationRolesRepository)