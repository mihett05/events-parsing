from domain.organizations.dtos import CreateOrganizationTokenDto
from domain.organizations.entities import OrganizationToken
from domain.organizations.repositories import OrganizationTokensRepository
from domain.users.entities import User
from domain.users.role_getter import RoleGetter

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.organizations.permissions import (
    OrganizationLinkPermissionProvider,
)
from application.transactions import TransactionsGateway


class CreateOrganizationTokenUseCase:
    def __init__(
        self,
        repository: OrganizationTokensRepository,
        permission_builder: PermissionBuilder,
        transaction: TransactionsGateway,
        role_getter: RoleGetter,
    ):
        self.__repository = repository
        self.__builder = permission_builder
        self.__transaction = transaction
        self.__role_getter = role_getter

    async def __call__(self, actor: User) -> OrganizationToken:
        async with self.__transaction:
            role = await self.__role_getter(actor)
            self.__builder.providers(OrganizationLinkPermissionProvider(role)).add(
                PermissionsEnum.CAN_CREATE_ORGANIZATION_LINK
            ).apply()
            return await self.__repository.create(CreateOrganizationTokenDto(actor.id))
