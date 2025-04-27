from domain.organizations.dtos import CreateOrganizationDto
from domain.organizations.entities import Organization
from domain.organizations.repositories import (
    OrganizationsRepository,
)
from domain.users.entities import User


class CreateOrganizationUseCase:
    def __init__(self, repository: OrganizationsRepository):
        self.__repository = repository

    async def __call__(
        self, dto: CreateOrganizationDto, actor: User | None
    ) -> Organization:
        return await self.__repository.create(dto)
