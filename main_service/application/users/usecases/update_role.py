from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.users.permissions.user import UserPermissionProvider
from application.users.usecases import ReadUserRolesUseCase
from application.users.usecases.read_role import ReadUserRoleUseCase
from domain.users.entities import UserOrganizationRole, User
from domain.users.repositories import UserOrganizationRolesRepository

from application.transactions import TransactionsGateway



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

    async def __call__(self, dto: UserOrganizationRole, actor: User | None) -> UserOrganizationRole:
        async with self.__transaction:
            roles = await self.__read_roles_use_case(actor.id)
            self.__builder.providers(
                UserPermissionProvider(dto.organization_id, roles)
            ).add(PermissionsEnum.CAN_UPDATE_ROLE).apply()
            role = await self.__repository.read(dto.user_id, dto.organization_id)
            role.role = dto.role
            return await self.__repository.update(role)