from main_service.application.transactions import TransactionsGateway

from main_service.domain.organizations.entities import UserOrganizationRole
from main_service.domain.organizations.repositories import UserOrganizationRolesRepository
from main_service.domain.users.entities import User


class DeleteUserOrganizationRoleUsecase:
    def __init__(self, repository: UserOrganizationRolesRepository, tx: TransactionsGateway):
        self.__repository = repository
        self.__transaction = tx

    async def __call__(self, id_: int, actor: User) -> UserOrganizationRole:
        async with self.__transaction:
            role = await self.__repository.read(id_)
            await self.__repository.delete(role)
        return role