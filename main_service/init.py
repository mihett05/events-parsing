import asyncio
from uuid import uuid4

from application.auth.dtos import RegisterUserDto
from application.auth.usecases import CreateUserWithPasswordUseCase
from dishka import AsyncContainer
from domain.organizations.dtos import CreateOrganizationDto
from domain.organizations.entities import Organization
from domain.organizations.repositories import OrganizationsRepository
from domain.users.entities import User, UserOrganizationRole
from domain.users.enums import RoleEnum
from domain.users.exceptions import (
    UserNotFoundError,
    UserRoleNotFoundError,
)
from domain.users.repositories import (
    UserOrganizationRolesRepository,
    UsersRepository,
)
from infrastructure.config import Config
from infrastructure.providers.container import create_container


async def _create_admin(
    config: Config,
    users_repository: UsersRepository,
    create_user: CreateUserWithPasswordUseCase,
):
    dto = RegisterUserDto(email=config.admin_username, password=config.admin_password)
    try:
        user = await users_repository.read_by_email(dto.email)
    except UserNotFoundError:
        user = await create_user(dto)
    finally:
        await users_repository.change_user_active_status(user.id, True)
        return user


async def _create_organization(
    config: Config,
    organizations_repository: OrganizationsRepository,
    admin: User,
):
    dto = CreateOrganizationDto(admin.id, config.base_organization, uuid4())
    return await organizations_repository.find(
        admin.id
    ) or await organizations_repository.create(dto)


async def _create_role(
    roles_repository: UserOrganizationRolesRepository,
    admin: User,
    organization: Organization,
):
    dto = UserOrganizationRole(
        user_id=admin.id,
        organization_id=organization.id,
        role=RoleEnum.SUPER_OWNER,
    )
    try:
        return await roles_repository.read(admin.id, organization.id)
    except UserRoleNotFoundError:
        return await roles_repository.create(dto)


async def init(container: AsyncContainer):
    async with container() as nested:
        config = await nested.get(Config)
        create_user = await nested.get(CreateUserWithPasswordUseCase)

        users_repository = await nested.get(UsersRepository)
        organizations_repository = await nested.get(OrganizationsRepository)
        roles_repository = await nested.get(UserOrganizationRolesRepository)

        admin = await _create_admin(config, users_repository, create_user)
        organization = await _create_organization(
            config, organizations_repository, admin
        )
        await _create_role(roles_repository, admin, organization)


if __name__ == "__main__":
    asyncio.run(init(create_container()))
