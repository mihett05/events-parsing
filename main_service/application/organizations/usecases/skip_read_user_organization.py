from main_service.domain.organizations.entities import UserOrganizationRole
from main_service.domain.organizations.repositories import (
    UserOrganizationRolesRepository,
)


class ReadUserOrganizationRoleUsecase:
    def __init__(self, repository: UserOrganizationRolesRepository):
        self.__repository = repository

    async def __call__(self, id_: int) -> UserOrganizationRole:
        return await self.__repository.read(id_)
