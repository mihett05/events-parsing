from domain.exceptions import EntityAccessDenied
from domain.users.entities import User, UserOrganizationRole
from domain.users.exceptions import UserRoleNotFoundError
from domain.users.repositories import UserOrganizationRolesRepository

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
    ):
        self.__repository = repository
        self.__read_role_use_case = read_role_use_case
        self.__transaction = transaction
        self.__builder = permission_builder

    async def __call__(
        self, dto: DeleteUserRoleDto, actor: User
    ) -> UserOrganizationRole:
        async with self.__transaction:
            roles = await self.__repository.read(actor.id, dto.organization_id)
            self.__builder.providers(
                UserRolesPermissionProvider(dto.organization_id, roles)
            ).add(PermissionsEnum.CAN_DELETE_ROLE).apply()
            if role := await self.__repository.read(
                dto.user_id, dto.organization_id
            ):
                return await self.__repository.delete(role)
            raise UserRoleNotFoundError
