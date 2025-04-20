from main_service.domain.organizations.dtos import CreateUserOrganizationRoleDto
from main_service.domain.organizations.entities import UserOrganizationRole
from main_service.domain.organizations.repositories import (
    UserOrganizationRolesRepository,
)


class CreateUserOrganizationRoleUsecase:
    def __init__(self, repository: UserOrganizationRolesRepository):
        self.__repository = repository

    async def __call__(
        self, dto: CreateUserOrganizationRoleDto
    ) -> UserOrganizationRole:
        return await self.__repository.create(dto)
