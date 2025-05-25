import pytest
import pytest_asyncio
from application.users.dtos import DeleteUserRoleDto, UpdateUserDto
from dishka import AsyncContainer
from domain.organizations.entities import Organization
from domain.users.dtos import (
    ReadAllUsersDto,
)
from domain.users.entities import User, UserOrganizationRole
from domain.users.enums import RoleEnum
from domain.users.exceptions import UserRoleAlreadyExistsError, UserRoleNotFoundError
from domain.users.repositories import (
    UserOrganizationRolesRepository,
    UsersRepository,
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
        await users_repository.create(user_entity) for user_entity in get_user_entities
    ]


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare(
    pytestconfig: pytest.Config,
    users_repository: UsersRepository,
    user_organization_roles_repository: UserOrganizationRolesRepository,
):
    if pytestconfig.getoption("--integration", default=False):
        return
    await users_repository.clear()  # noqa
    await user_organization_roles_repository.clear()  # noqa


@pytest_asyncio.fixture(scope="function", autouse=True)
async def teardown(
    pytestconfig: pytest.Config,
    users_repository: UsersRepository,
    user_organization_roles_repository: UserOrganizationRolesRepository,
):
    yield
    if pytestconfig.getoption("--integration", default=False):
        return
    await users_repository.clear()  # noqa
    await user_organization_roles_repository.clear()  # noqa


@pytest_asyncio.fixture(scope="function", autouse=True)
async def create_user_role_dto(
    get_user_entity: User,
    get_admin_organization: Organization,
) -> UserOrganizationRole:
    return UserOrganizationRole(
        user_id=get_user_entity.id,
        organization_id=get_admin_organization.id,
        role=RoleEnum.ADMIN,
    )


@pytest_asyncio.fixture(scope="function", autouse=True)
async def update_user_role_dto(
    get_user_entity: User,
    get_admin_organization: Organization,
) -> UserOrganizationRole:
    return UserOrganizationRole(
        user_id=get_user_entity.id,
        organization_id=get_admin_organization.id,
        role=RoleEnum.OWNER,
    )


@pytest_asyncio.fixture
async def delete_user_role_dto(
    get_user_entity: User, get_admin_organization: Organization
) -> DeleteUserRoleDto:
    return DeleteUserRoleDto(
        user_id=get_user_entity.id, organization_id=get_admin_organization.id
    )


@pytest_asyncio.fixture
async def user_organization_roles_repository(
    container: AsyncContainer,
) -> UserOrganizationRolesRepository:
    async with container() as nested:
        yield await nested.get(UserOrganizationRolesRepository)


@pytest_asyncio.fixture
async def user_with_update_dto(create_user) -> tuple[User, UpdateUserDto]:
    return create_user, UpdateUserDto(
        user_id=create_user.id,
        fullname="Romanov Roman Romacnovich",
    )
