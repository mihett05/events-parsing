from domain.exceptions import EntityAccessDenied
from domain.users.entities import User, UserOrganizationRole
from domain.users.repositories import UserOrganizationRolesRepository

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.transactions import TransactionsGateway
from application.users.permissions.user import UserRolesPermissionProvider
from application.users.usecases.read_role import ReadUserRoleUseCase


class UpdateUserRoleUseCase:
    def __init__(
        self,
        repository: UserOrganizationRolesRepository,
        read_role_use_case: ReadUserRoleUseCase,
        transaction: TransactionsGateway,
        permission_builder: PermissionBuilder,
    ):
        self.__repository = repository
        self.__read_role_use_case = read_role_use_case
        self.__transaction = transaction
        self.__builder = permission_builder

    async def __call__(
        self, entity: UserOrganizationRole, actor: User
    ) -> UserOrganizationRole:
        async with self.__transaction:
            roles = await self.__repository.read_all(actor.id)
            self.__builder.providers(
                UserRolesPermissionProvider(entity.organization_id, roles)
            ).add(PermissionsEnum.CAN_UPDATE_ROLE).apply()
            role = await self.__repository.read(entity.user_id, entity.organization_id)
            role.role = entity.role
            return await self.__repository.update(role)
