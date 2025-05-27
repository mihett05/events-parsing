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


class ReadOrganizationTokenUseCase:
    """
    Сценарий получения конкретного токена организации.

    Обеспечивает доступ к токену с проверкой прав доступа
    на чтение организационных ссылок.
    """
    def __init__(
        self,
        repository: OrganizationTokensRepository,
        permission_builder: PermissionBuilder,
        role_getter: RoleGetter,
    ):
        """
        Инициализирует сценарий работы с организацией.
        """

        self.__repository = repository
        self.__builder = permission_builder
        self.__role_getter = role_getter

    async def __call__(self, token_id: UUID, actor: User) -> OrganizationToken:
        """
        Основная точка входа для выполнения сценария.
        """

        actor_role = await self.__role_getter(actor)
        self.__builder.providers(OrganizationLinkPermissionProvider(actor_role)).add(
            PermissionsEnum.CAN_READ_ORGANIZATION_LINK
        ).apply()
        return await self.__repository.read(token_id)
