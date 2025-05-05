from domain.users.entities import User, UserOrganizationRole
from domain.users.repositories import UserOrganizationRolesRepository

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.transactions import TransactionsGateway
from application.users.permissions.user import UserPermissionProvider
from application.users.usecases import ReadUserRolesUseCase


class CreateUserRoleUseCase:
    def __init__(
        self,
        repository: UserOrganizationRolesRepository,
        permission_builder: PermissionBuilder,
        transaction: TransactionsGateway,
        read_roles_use_case: ReadUserRolesUseCase,
    ):
        self.__repository = repository
        self.__builder = permission_builder
        self.__transaction = transaction
        self.__read_roles_use_case = read_roles_use_case

    async def __call__(
        self, role: UserOrganizationRole, actor: User | None
    ) -> UserOrganizationRole:
        async with self.__transaction:
            roles = await self.__read_roles_use_case(actor.id)
            self.__builder.providers(
                UserPermissionProvider(role.organization_id, roles)
            ).add(PermissionsEnum.CAN_CREATE_ROLE).apply()
        return await self.__repository.create(role)
