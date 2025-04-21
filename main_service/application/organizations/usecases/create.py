from main_service.domain.organizations.dtos import CreateOrganizationDto
from main_service.domain.organizations.entities import Organization
from main_service.domain.organizations.repositories import (
    OrganizationRepository,
)
from main_service.domain.users.entities import User


class CreateOrganizationUseCase:
    def __init__(self, repository: OrganizationRepository):
        self.__repository = repository

    async def __call__(
        self, dto: CreateOrganizationDto, actor: User | None
    ) -> Organization:
        return await self.__repository.create(dto)
