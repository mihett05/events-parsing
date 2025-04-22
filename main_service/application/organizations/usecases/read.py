from main_service.domain.organizations.entities import Organization
from main_service.domain.organizations.repositories import (
    OrganizationsRepository,
)


class ReadOrganizationUseCase:
    def __init__(self, repository: OrganizationsRepository):
        self.__repository = repository

    async def __call__(self, organization_id: int) -> Organization:
        return await self.__repository.read(organization_id)
