from application.users.usecases.read_role import ReadUserRoleUseCase
from domain.users.entities import UserOrganizationRole, User
from domain.users.repositories import UserOrganizationRolesRepository

from application.transactions import TransactionsGateway



class UpdateUserRoleUseCase:
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
            role = await self.__repository.read(dto.user_id, dto.organization_id)
            role.role = dto.role
            return await self.__repository.update(role)