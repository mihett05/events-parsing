from domain.organizations.entities import Organization
from domain.organizations.repositories import (
    OrganizationsRepository,
)


class ReadOrganizationUseCase:
    def __init__(self, repository: OrganizationsRepository):
        self.__repository = repository

    async def __call__(self, organization_id: int) -> Organization:
        return await self.__repository.read(organization_id)
