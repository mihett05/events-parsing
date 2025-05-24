from typing import Any, Callable, Coroutine
from uuid import uuid4

import application.auth.usecases as auth_usecases
import application.users.usecases as user_usecases
import pytest
import pytest_asyncio
from application.auth.dtos import RegisterUserDTO
from application.auth.usecases import CreateUserWithPasswordUseCase, RegisterUseCase
from dishka import AsyncContainer
from domain.organizations.dtos import CreateOrganizationDto
from domain.organizations.entities import Organization
from domain.organizations.repositories import OrganizationsRepository
from domain.users.entities import User, UserOrganizationRole, UserSettings
from domain.users.enums import RoleEnum
from domain.users.repositories import UserOrganizationRolesRepository, UsersRepository
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

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
async def users_repository(
    container: AsyncContainer,
) -> auth_usecases.RegisterUseCase:
    async with container() as nested:
        yield await nested.get(UsersRepository)


@pytest_asyncio.fixture
async def roles_repository(
    container: AsyncContainer,
) -> auth_usecases.RegisterUseCase:
    async with container() as nested:
        yield await nested.get(UserOrganizationRolesRepository)


@pytest_asyncio.fixture
async def organizations_repository(
    container: AsyncContainer,
) -> auth_usecases.RegisterUseCase:
    async with container() as nested:
        yield await nested.get(OrganizationsRepository)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_(
    pytestconfig: pytest.Config,
    users_repository: UsersRepository,
    roles_repository: UserOrganizationRolesRepository,
    organizations_repository: OrganizationsRepository,
):
    if not pytestconfig.getoption("--integration", default=False):
        await users_repository.clear()  # noqa
        await roles_repository.clear()  # noqa
        await organizations_repository.clear()  # noqa


@pytest_asyncio.fixture(scope="function", autouse=True)
async def teardown_(
    pytestconfig: pytest.Config,
    users_repository: UsersRepository,
    roles_repository: UserOrganizationRolesRepository,
    organizations_repository: OrganizationsRepository,
):
    yield
    if not pytestconfig.getoption("--integration", default=False):
        await users_repository.clear()  # noqa
        await roles_repository.clear()  # noqa
        await organizations_repository.clear()  # noqa


@pytest_asyncio.fixture(scope="function", autouse=True)
async def init_entities(
    setup_data,  # noqa
    prepare_,  # noqa
    container: AsyncContainer,
) -> tuple[User, Organization, UserOrganizationRole]:
    async with container() as nested:
        _create_user_dto = RegisterUserDTO(
            email="admin@admin.com", password="admin", is_active=True
        )
        admin = await (await nested.get(CreateUserWithPasswordUseCase))(
            _create_user_dto
        )

        _create_organization_dto = CreateOrganizationDto(
            token=uuid4(), title="admin organization", owner_id=admin.id
        )
        organization = await (await nested.get(OrganizationsRepository)).create(
            _create_organization_dto
        )

        _create_role_dto = UserOrganizationRole(
            user_id=admin.id, organization_id=organization.id, role=RoleEnum.SUPER_OWNER
        )
        role = await (await nested.get(UserOrganizationRolesRepository)).create(
            _create_role_dto
        )

    return admin, organization, role


@pytest_asyncio.fixture(scope="function")
async def get_admin(init_entities) -> User:
    admin, _, _ = init_entities
    return admin


@pytest_asyncio.fixture(scope="function")
async def get_admin_organization(init_entities) -> Organization:
    _, organization, _ = init_entities
    return organization


@pytest_asyncio.fixture(scope="function")
async def get_admin_role(init_entities) -> UserOrganizationRole:
    _, _, role = init_entities
    return role


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
    register_user1_dto: RegisterUserDTO,
    register_usecase: RegisterUseCase,
) -> Callable[..., Coroutine[Any, Any, User]]:
    async def _factory() -> User:
        token1 = await register_usecase(register_user1_dto)
        return token1.user

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
) -> user_usecases.CreateUserRoleUseCase:
    async with container() as nested:
        yield await nested.get(user_usecases.CreateUserRoleUseCase)


@pytest_asyncio.fixture
async def create_organization(
    create_organization_dto: CreateOrganizationDto,
    organizations_repository: OrganizationsRepository,
) -> Organization:
    return await organizations_repository.create(create_organization_dto)


@pytest_asyncio.fixture
async def create_organization_dto(create_user1) -> CreateOrganizationDto:
    user = await create_user1()
    return CreateOrganizationDto(
        title="Test Organization",
        owner_id=user.id,
    )


@pytest_asyncio.fixture
async def organizations_repository(
    container: AsyncContainer,
) -> OrganizationsRepository:
    async with container() as request_container:
        yield await request_container.get(OrganizationsRepository)


@pytest_asyncio.fixture
async def create_user(
    get_user_entity: User,
    users_repository: UsersRepository,
) -> Callable[..., Coroutine[Any, Any, User]]:
    async def _factory():
        user = await users_repository.create(get_user_entity)
        return user

    return _factory
