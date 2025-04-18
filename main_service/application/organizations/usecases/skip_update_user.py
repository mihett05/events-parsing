from main_service.application.organizations.dtos import UpdateUserOrganizationRoleDto
from main_service.application.transactions import TransactionsGateway
from main_service.domain.organizations.entities import UserOrganizationRole
from main_service.domain.organizations.repositories import UserOrganizationRolesRepository
from main_service.domain.users.entities import User


class UpdateUserOrganizationRoleUsecase:
    def __init__(self, repository: UserOrganizationRolesRepository, tx: TransactionsGateway):
        self.__repository = repository
        self.__transaction = tx

    async def __call__(self, dto: UpdateUserOrganizationRoleDto, actor: User) -> UserOrganizationRole:
        async with self.__transaction:
            role = await self.__repository.read(dto.id)
            role.role = dto.role
            await self.__repository.update(role)
        return role