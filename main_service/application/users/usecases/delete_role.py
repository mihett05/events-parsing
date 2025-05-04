from domain.users.entities import UserOrganizationRole, User
from domain.users.repositories import UserOrganizationRolesRepository

from application.transactions import TransactionsGateway


from .read_role import ReadUserRoleUseCase


class DeleteUserRoleUseCase:
    def __init__(
        self,
        repository: UserOrganizationRolesRepository,
        read_role_use_case: ReadUserRoleUseCase,
        tx: TransactionsGateway,
    ):
        self.__repository = repository
        self.__read_role_use_case = read_role_use_case
        self.__transaction = tx

    async def __call__(self, dto: UserOrganizationRole, actor: User | None) -> UserOrganizationRole:
        async with self.__transaction:
            role = await self.__read_role_use_case(dto.user_id, dto.organization_id)
            return await self.__repository.delete(role)
