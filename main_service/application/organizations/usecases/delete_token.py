from uuid import UUID

from domain.organizations.entities import OrganizationToken
from domain.organizations.repositories import OrganizationTokensRepository
from domain.users.entities import User
from domain.users.role_getter import RoleGetter

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.organizations.permissions import (
    OrganizationLinkPermissionProvider,
)
from application.organizations.usecases.read_token import (
    ReadOrganizationTokenUseCase,
)
from application.transactions import TransactionsGateway


class DeleteOrganizationTokenUseCase:
    """Сценарий удаления токена организации.
    Обеспечивает безопасное удаление токена-приглашения в организацию
    с проверкой прав доступа инициатора операции.
    """
    def __init__(
        self,
        repository: OrganizationTokensRepository,
        transaction: TransactionsGateway,
        read_use_case: ReadOrganizationTokenUseCase,
        permission_builder: PermissionBuilder,
        role_getter: RoleGetter,
    ):
        """
        Инициализация зависимостей сценария.
        """
        self.__repository = repository
        self.__transaction = transaction
        self.__read_use_case = read_use_case
        self.__builder = permission_builder
        self.__role_getter = role_getter

    async def __call__(self, token_id: UUID, actor: User) -> OrganizationToken:
        """
        Выполнение операции удаления токена.
        """
        async with self.__transaction:
            actor_role = await self.__role_getter(actor)
            self.__builder.providers(
                OrganizationLinkPermissionProvider(actor_role)
            ).add(PermissionsEnum.CAN_DELETE_ORGANIZATION_LINK).apply()
            token = await self.__read_use_case(token_id, actor)
            return await self.__repository.delete(token)
