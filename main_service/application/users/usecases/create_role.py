from domain.users.entities import UserOrganizationRole, User
from domain.users.repositories import UserOrganizationRolesRepository


class CreateUserRoleUseCase:
    def __init__(self, repository: UserOrganizationRolesRepository):
        self.__repository = repository

    async def __call__(self, role: UserOrganizationRole, actor: User | None) -> UserOrganizationRole:
        return await self.__repository.create(role)
