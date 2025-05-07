from uuid import UUID

from domain.organizations.entities import OrganizationToken
from domain.organizations.repositories import OrganizationTokensRepository
from domain.users.entities import User

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.organizations.permissions import OrganizationLinkPermissionProvider
from application.organizations.usecases.read_token import (
    ReadOrganizationTokenUseCase,
)
from application.transactions import TransactionsGateway
from application.users.usecases import ReadUserRolesUseCase


class DeleteOrganizationTokenUseCase:
    def __init__(
        self,
        repository: OrganizationTokensRepository,
        transaction: TransactionsGateway,
        read_use_case: ReadOrganizationTokenUseCase,
        read_role_use_case: ReadUserRolesUseCase,
        permission_builder: PermissionBuilder,
    ):
        self.__repository = repository
        self.__transaction = transaction
        self.__read_use_case = read_use_case
        self.__builder = permission_builder
        self.__read_roles_use_case = read_role_use_case

    async def __call__(self, token_id: UUID, actor: User) -> OrganizationToken:
        async with self.__transaction:
            roles = await self.__read_roles_use_case(actor.id)
            self.__builder.providers(OrganizationLinkPermissionProvider(roles)).add(
                PermissionsEnum.CAN_DELETE_ORGANIZATION_LINK
            ).apply()
            token = await self.__read_use_case(token_id, actor)
            return await self.__repository.delete(token)
