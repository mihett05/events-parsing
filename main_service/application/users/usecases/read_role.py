from domain.users.entities import UserOrganizationRole
from domain.users.repositories import UserOrganizationRolesRepository


class ReadUserRoleUseCase:
    def __init__(self, repository: UserOrganizationRolesRepository):
        self.__repository = repository

    async def __call__(
        self, user_id: int, organization_id: int
    ) -> UserOrganizationRole:
        return await self.__repository.read(user_id, organization_id)
