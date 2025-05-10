import pytest_asyncio
from application.users.dtos import UpdateUserDto, DeleteUserRoleDto
from dishka import AsyncContainer
from domain.users.dtos import (
    ReadAllUsersDto,
)
from domain.users.entities import User, UserOrganizationRole
from domain.users.enums import RoleEnum
from domain.users.repositories import UsersRepository, UserOrganizationRolesRepository


@pytest_asyncio.fixture
async def get_user_entity() -> User:
    return User(
        email="test@test.com",
        fullname="Ivanov Ivan Ivanovich",
    )


@pytest_asyncio.fixture
async def get_user_entities() -> list[User]:
    return [
        User(
            email=f"test{i}@test.com",
            fullname=f"Iivan{i}",
        )
        for i in range(8)
    ]


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


@pytest_asyncio.fixture
async def get_user_role_entity() -> UserOrganizationRole:
    return UserOrganizationRole(user_id=1, organization_id=1, role=RoleEnum.SUPER_OWNER)

@pytest_asyncio.fixture
async def update_user_role_entity() -> UserOrganizationRole:
    return UserOrganizationRole(
        user_id=1,
        organization_id=1,
        role = RoleEnum.PUBLIC
    )

@pytest_asyncio.fixture
async def delete_user_role_dto() -> DeleteUserRoleDto:
    return DeleteUserRoleDto(
        user_id=1,
        organization_id=1
    )

@pytest_asyncio.fixture
async def user_organization_roles_repository(container: AsyncContainer) -> UserOrganizationRolesRepository:
    async with container() as nested:
        yield await nested.get(UserOrganizationRolesRepository)


@pytest_asyncio.fixture
async def create_user_role(
    get_role_entity: UserOrganizationRole,
    roles_repository: UserOrganizationRolesRepository,
) -> UserOrganizationRole:
    role = await roles_repository.create(get_role_entity)
    return role