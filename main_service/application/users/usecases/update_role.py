from domain.users.entities import User, UserOrganizationRole
from domain.users.repositories import UserOrganizationRolesRepository
from domain.users.role_getter import RoleGetter

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.transactions import TransactionsGateway
from application.users.permissions.user import UserRolesPermissionProvider


class UpdateUserRoleUseCase:
    def __init__(
        self,
        repository: UserOrganizationRolesRepository,
        transaction: TransactionsGateway,
        permission_builder: PermissionBuilder,
        role_getter: RoleGetter,
    ):
        self.__repository = repository
        self.__transaction = transaction
        self.__builder = permission_builder
        self.__role_getter = role_getter

    async def __call__(
        self, entity: UserOrganizationRole, actor: User
    ) -> UserOrganizationRole:
        async with self.__transaction:
            actor_role = await self.__role_getter(actor, entity.organization_id)
            self.__builder.providers(
                UserRolesPermissionProvider(entity.organization_id, actor_role)
            ).add(PermissionsEnum.CAN_UPDATE_ROLE).apply()
            return await self.__repository.update(entity)
