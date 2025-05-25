from domain.users.entities import User, UserOrganizationRole
from domain.users.enums import roles_delete_priorities_table
from domain.users.exceptions import UserAccessDenied, UserRoleNotFoundError
from domain.users.repositories import UserOrganizationRolesRepository
from domain.users.role_getter import RoleGetter

from application.transactions import TransactionsGateway

from ...auth.enums import PermissionsEnum
from ...auth.permissions import PermissionBuilder
from ..dtos import DeleteUserRoleDto
from ..permissions.user import UserRolesPermissionProvider
from .read_role import ReadUserRoleUseCase


class DeleteUserRoleUseCase:
    def __init__(
        self,
        repository: UserOrganizationRolesRepository,
        read_role_use_case: ReadUserRoleUseCase,
        permission_builder: PermissionBuilder,
        transaction: TransactionsGateway,
        role_getter: RoleGetter,
    ):
        self.__repository = repository
        self.__read_role_use_case = read_role_use_case
        self.__transaction = transaction
        self.__builder = permission_builder
        self.__role_getter = role_getter

    async def __call__(
        self, dto: DeleteUserRoleDto, actor: User
    ) -> UserOrganizationRole:
        async with self.__transaction:
            actor_role = await self.__role_getter(actor, dto.organization_id)
            self.__builder.providers(
                UserRolesPermissionProvider(dto.organization_id, actor_role)
            ).add(PermissionsEnum.CAN_DELETE_ROLE).apply()
            if role := await self.__repository.read(dto.user_id, dto.organization_id):
                if (
                    roles_delete_priorities_table[actor_role.role]
                    > roles_delete_priorities_table[role.role]
                ):
                    return await self.__repository.delete(role)
                raise UserAccessDenied
            raise UserRoleNotFoundError
