from domain.users.entities import User, UserOrganizationRole
from domain.users.enums import RoleEnum, roles_delete_priorities_table
from domain.users.exceptions import UserAccessDenied
from domain.users.repositories import UserOrganizationRolesRepository
from domain.users.role_getter import RoleGetter

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
        role_getter: RoleGetter,
    ):
        self.__repository = repository
        self.__builder = permission_builder
        self.__transaction = transaction
        self.__role_getter = role_getter

    async def __call__(
        self, role: UserOrganizationRole, actor: User
    ) -> UserOrganizationRole:
        async with self.__transaction:
            actor_role = await self.__role_getter(actor, role.organization_id)
            self.__builder.providers(
                UserRolesPermissionProvider(role.organization_id, actor_role)
            ).add(PermissionsEnum.CAN_CREATE_ROLE).apply()
            if role.role != RoleEnum.OWNER:
                if (
                    roles_delete_priorities_table[actor_role.role]
                    < roles_delete_priorities_table[role.role]
                ):
                    return await self.__repository.create(role)
            raise UserAccessDenied
