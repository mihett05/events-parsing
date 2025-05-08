from domain.exceptions import EntityAccessDenied
from domain.users.entities import User, UserOrganizationRole
from domain.users.repositories import UserOrganizationRolesRepository

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.transactions import TransactionsGateway
from application.users.permissions.user import UserRolesPermissionProvider
from application.users.usecases import ReadUserRolesUseCase
from application.users.usecases.read_role import ReadUserRoleUseCase


class UpdateUserRoleUseCase:
    def __init__(
        self,
        repository: UserOrganizationRolesRepository,
        read_role_use_case: ReadUserRoleUseCase,
        transaction: TransactionsGateway,
        permission_builder: PermissionBuilder,
        read_roles_use_case: ReadUserRolesUseCase,
    ):
        self.__repository = repository
        self.__read_role_use_case = read_role_use_case
        self.__transaction = transaction
        self.__builder = permission_builder
        self.__read_roles_use_case = read_roles_use_case

    async def __call__(
        self, dto: UserOrganizationRole, actor: User
    ) -> UserOrganizationRole:
        async with self.__transaction:
            roles = await self.__read_roles_use_case(actor.id)
            self.__builder.providers(
                UserRolesPermissionProvider(dto.organization_id, roles)
            ).add(PermissionsEnum.CAN_UPDATE_ROLE).apply()
            user_role_changed = False
            for role in roles:
                if role.organization_id == dto.organization_id:
                    role.role = dto.role
                    user_role_changed = role
                    break
            if not user_role_changed:
                raise EntityAccessDenied
            return await self.__repository.update(user_role_changed)
