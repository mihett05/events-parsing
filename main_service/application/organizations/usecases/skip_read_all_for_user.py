from typing import List

from main_service.domain.organizations.dtos import ReadUserOrganizationRolesDto
from main_service.domain.organizations.entities import UserOrganizationRole
from main_service.domain.organizations.repositories import (
    UserOrganizationRolesRepository,
)


class ReadAllUserOrganizationUsecase:
    def __init__(self, repository: UserOrganizationRolesRepository):
        self.__repository = repository

    async def __call__(
        self, dto: ReadUserOrganizationRolesDto
    ) -> List[UserOrganizationRole]:
        return await self.__repository.read_all(dto)
