from domain.users.entities import User, UserOrganizationRole
from domain.users.repositories import UserOrganizationRolesRepository

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.transactions import TransactionsGateway
from application.users.permissions.user import UserRolesPermissionProvider


class CreateUserRoleUseCase:
    def __init__(
        self,
        repository: UserOrganizationRolesRepository,
        permission_builder: PermissionBuilder,
        transaction: TransactionsGateway,
    ):
        self.__repository = repository
        self.__builder = permission_builder
        self.__transaction = transaction

    async def __call__(
        self, role: UserOrganizationRole, actor: User
    ) -> UserOrganizationRole:
        async with self.__transaction:
            roles = await self.__repository.read(actor.id, role.organization_id)
            self.__builder.providers(
                UserRolesPermissionProvider(role.organization_id, roles)
            ).add(PermissionsEnum.CAN_CREATE_ROLE).apply()
            return await self.__repository.create(role)
