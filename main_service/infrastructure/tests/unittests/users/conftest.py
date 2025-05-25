import pytest_asyncio

from application.users.dtos import DeleteUserRoleDto, UpdateUserDto
from domain.organizations.entities import Organization
from domain.users.dtos import (
    ReadAllUsersDto,
)
from domain.users.entities import User, UserOrganizationRole
from domain.users.enums import RoleEnum
from domain.users.repositories import (
    UserOrganizationRolesRepository,
)


@pytest_asyncio.fixture
async def read_all_users_dto() -> ReadAllUsersDto:
    return ReadAllUsersDto(page=0, page_size=8)


@pytest_asyncio.fixture(scope="function")
async def create_user_role_dto(
        get_user_entity: User,
        get_admin_organization: Organization,
) -> UserOrganizationRole:
    return UserOrganizationRole(
        user_id=get_user_entity.id,
        organization_id=get_admin_organization.id,
        role=RoleEnum.ADMIN,
    )


@pytest_asyncio.fixture(scope="function")
async def update_user_dto(
        get_user_entity: User,
) -> UpdateUserDto:
    return UpdateUserDto(get_user_entity.id, fullname="Nigger")

@pytest_asyncio.fixture(scope="function")
async def create_user_role(
        create_user_role_dto: UserOrganizationRole,
        roles_repository: UserOrganizationRolesRepository,
) -> UserOrganizationRole:
    return await roles_repository.create(create_user_role_dto)


@pytest_asyncio.fixture(scope="function")
async def update_user_role_dto(
        get_user_entity: User,
        get_admin_organization: Organization,
) -> UserOrganizationRole:
    return UserOrganizationRole(
        user_id=get_user_entity.id,
        organization_id=get_admin_organization.id,
        role=RoleEnum.OWNER,
    )


@pytest_asyncio.fixture(scope="function")
async def delete_user_role_dto(
        get_user_entity: User, get_admin_organization: Organization
) -> DeleteUserRoleDto:
    return DeleteUserRoleDto(
        user_id=get_user_entity.id, organization_id=get_admin_organization.id
    )
