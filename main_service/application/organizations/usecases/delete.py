from domain.organizations.entities import Organization
from domain.organizations.repositories import OrganizationsRepository
from domain.users.entities import User
from domain.users.role_getter import RoleGetter

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.organizations.permissions import OrganizationPermissionProvider
from application.organizations.usecases.read import ReadOrganizationUseCase
from application.transactions import TransactionsGateway
from application.users.usecases.read_all_roles import ReadUserRolesUseCase


class DeleteOrganizationUseCase:
    """Сценарий удаления организации.

    Обеспечивает процесс удаления организации с проверкой прав доступа.
    Включает валидацию прав пользователя и целостность данных при удалении.
    """

    def __init__(
        self,
        repository: OrganizationsRepository,
        transaction: TransactionsGateway,
        permission_builder: PermissionBuilder,
        read_roles_use_case: ReadUserRolesUseCase,
        read_organization_use_case: ReadOrganizationUseCase,
        role_getter: RoleGetter,
    ):
        """
        Инициализация сценария удаления.
        """
        self.__repository = repository
        self.__transaction = transaction
        self.__builder = permission_builder
        self.__read_roles_use_case = read_roles_use_case
        self.__read_organization_use_case = read_organization_use_case
        self.__role_getter = role_getter

    async def __call__(self, organization_id: int, actor: User) -> Organization:
        """
        Выполнение операции удаления организации.
        """
        async with self.__transaction:
            organization = await self.__read_organization_use_case(organization_id)
            actor_role = await self.__role_getter(actor, organization_id)
            self.__builder.providers(
                OrganizationPermissionProvider(actor_role, organization_id)
            ).add(PermissionsEnum.CAN_DELETE_ORGANIZATION).apply()
            return await self.__repository.delete(organization)
