from datetime import datetime, timedelta
from uuid import uuid4

import application.auth.usecases as auth_usecases
import pytest
import pytest_asyncio
from application.auth.dtos import RegisterUserDto
from application.auth.usecases import CreateUserWithPasswordUseCase
from application.events.usecases import CreateEventUseCase
from application.transactions import TransactionsGateway
from dishka import AsyncContainer
from domain.events.dtos import CreateEventDto
from domain.events.entities import Event
from domain.events.enums import EventFormatEnum, EventTypeEnum
from domain.events.repositories import EventsRepository
from domain.organizations.dtos import CreateOrganizationDto
from domain.organizations.entities import Organization
from domain.organizations.repositories import OrganizationsRepository
from domain.users.entities import User, UserOrganizationRole
from domain.users.enums import RoleEnum
from domain.users.repositories import (
    UserOrganizationRolesRepository,
    UsersRepository,
)
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from infrastructure.database.postgres import Base
from infrastructure.mocks.repositories.crud import get_storage
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
async def setup_data(
    setup_db_tables, pytestconfig: pytest.Config, container: AsyncContainer
):
    if not pytestconfig.getoption("--integration", default=False):
        return
    engine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(
                text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE")
            )


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare(pytestconfig: pytest.Config):
    if not pytestconfig.getoption("--integration", default=False):
        get_storage(None, reset=True)
    yield
    if not pytestconfig.getoption("--integration", default=False):
        get_storage(None, reset=True)


@pytest_asyncio.fixture(scope="function")
async def users_repository(
    setup_data,
    prepare,
    container: AsyncContainer,
) -> auth_usecases.RegisterUseCase:
    async with container() as nested:
        yield await nested.get(UsersRepository)


@pytest_asyncio.fixture(scope="function")
async def roles_repository(
    setup_data,
    prepare,
    container: AsyncContainer,
) -> auth_usecases.RegisterUseCase:
    async with container() as nested:
        yield await nested.get(UserOrganizationRolesRepository)


@pytest_asyncio.fixture(scope="function")
async def organizations_repository(
    setup_data,
    prepare,
    container: AsyncContainer,
) -> auth_usecases.RegisterUseCase:
    async with container() as nested:
        yield await nested.get(OrganizationsRepository)


@pytest_asyncio.fixture(scope="function")
async def events_repository(
    container: AsyncContainer,
) -> EventsRepository:
    async with container() as nested:
        yield await nested.get(EventsRepository)


@pytest_asyncio.fixture(scope="function")
async def create_user_with_password(
    container: AsyncContainer,
) -> auth_usecases.CreateUserWithPasswordUseCase:
    async with container() as nested:
        yield await nested.get(CreateUserWithPasswordUseCase)


@pytest_asyncio.fixture(scope="function")
async def create_event_dto() -> CreateEventDto:
    date = datetime.now().date()
    return CreateEventDto(
        title="Example",
        type=EventTypeEnum.HACKATHON,
        format=EventFormatEnum.OFFLINE,
        location=None,
        description="Example Description",
        organization_id=None,
        end_date=date + timedelta(days=1),
        start_date=date,
        end_registration=date - timedelta(days=1),
    )


@pytest_asyncio.fixture(scope="function")
async def get_user_dto(
    setup_data,  # noqa
    prepare,  # noqa
    create_user_with_password: CreateUserWithPasswordUseCase,
) -> RegisterUserDto:
    return RegisterUserDto(email="public@public.com", password="public", is_active=True)


@pytest_asyncio.fixture(scope="function")
async def get_user_entity(
    setup_data,  # noqa
    prepare,  # noqa
    create_user_with_password: CreateUserWithPasswordUseCase,
    get_user_dto: RegisterUserDto,
) -> User:
    return await create_user_with_password(get_user_dto)


@pytest_asyncio.fixture(scope="function")
async def init_entities(
    create_event_dto,
    create_user_with_password: CreateUserWithPasswordUseCase,
    organizations_repository: OrganizationsRepository,
    roles_repository: UserOrganizationRolesRepository,
    events_repository: EventsRepository,
) -> tuple[User, Organization, UserOrganizationRole, Event]:
    _create_user_dto = RegisterUserDto(
        email="admin@admin.com", password="admin", is_active=True
    )
    get_admin = await create_user_with_password(_create_user_dto)

    _create_organization_dto = CreateOrganizationDto(
        token=uuid4(), title="admin organization", owner_id=get_admin.id
    )
    get_admin_organization = await organizations_repository.create(
        _create_organization_dto
    )

    _create_role_dto = UserOrganizationRole(
        user_id=get_admin.id,
        organization_id=get_admin_organization.id,
        role=RoleEnum.SUPER_OWNER,
    )
    get_admin_role = await roles_repository.create(_create_role_dto)

    create_event_dto.organization_id = get_admin_organization.id
    get_admin_event = await events_repository.create(create_event_dto)

    return get_admin, get_admin_organization, get_admin_role, get_admin_event


@pytest_asyncio.fixture(scope="function")
async def get_admin(
    init_entities: tuple[User, Organization, UserOrganizationRole, Event],
) -> User:
    user, *_ = init_entities
    return user


@pytest_asyncio.fixture(scope="function")
async def get_admin_organization(
    init_entities: tuple[User, Organization, UserOrganizationRole, Event],
) -> Organization:
    _, organization, *_ = init_entities
    return organization


@pytest_asyncio.fixture(scope="function")
async def get_admin_role(
    init_entities: tuple[User, Organization, UserOrganizationRole, Event],
) -> UserOrganizationRole:
    *_, role, _ = init_entities
    return role


@pytest_asyncio.fixture(scope="function")
async def get_admin_event(
    init_entities: tuple[User, Organization, UserOrganizationRole, Event],
) -> Event:
    *_, event = init_entities
    return event


@pytest_asyncio.fixture(scope="function")
async def get_user_entities(
    create_user_with_password: CreateUserWithPasswordUseCase,
) -> list[User]:
    return [
        await create_user_with_password(
            RegisterUserDto(email=f"test{i}@test.com", password="parol", is_active=True)
        )
        for i in range(8)
    ]
