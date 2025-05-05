from domain.users.entities import User, UserOrganizationRole
from domain.users.repositories import UserOrganizationRolesRepository


class CreateUserOrganizationRoleUseCase:
    def __init__(self, repository: UserOrganizationRolesRepository):
        self.__repository = repository

    async def __call__(
        self, role: UserOrganizationRole, actor: User
    ) -> UserOrganizationRole:
        return await self.__repository.create(role)
