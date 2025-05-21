from domain.organizations.dtos import CreateOrganizationTokenDto
from domain.organizations.entities import OrganizationToken
from domain.organizations.repositories import OrganizationTokensRepository
from domain.users.entities import User

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.organizations.permissions import (
    OrganizationLinkPermissionProvider,
)
from application.transactions import TransactionsGateway
from application.users.usecases import ReadUserRolesUseCase


class CreateOrganizationTokenUseCase:
    def __init__(
        self,
        repository: OrganizationTokensRepository,
        read_role_use_case: ReadUserRolesUseCase,
        permission_builder: PermissionBuilder,
        transaction: TransactionsGateway,
    ):
        self.__repository = repository
        self.__builder = permission_builder
        self.__transaction = transaction
        self.__read_roles_use_case = read_role_use_case

    async def __call__(self, actor: User) -> OrganizationToken:
        async with self.__transaction:
            roles = await self.__read_roles_use_case(actor.id)
            self.__builder.providers(
                OrganizationLinkPermissionProvider(roles)
            ).add(PermissionsEnum.CAN_CREATE_ORGANIZATION_LINK).apply()
            return await self.__repository.create(
                CreateOrganizationTokenDto(actor.id)
            )
