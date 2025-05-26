from domain.users.entities import UserOrganizationRole
from domain.users.repositories import UserOrganizationRolesRepository


class ReadUserRolesUseCase:
    def __init__(self, repository: UserOrganizationRolesRepository):
        self.__repository = repository

    async def __call__(self, user_id: int) -> list[UserOrganizationRole]:
        return await self.__repository.read_all(user_id)
