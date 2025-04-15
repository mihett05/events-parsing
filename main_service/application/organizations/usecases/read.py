from main_service.domain.organizations.entities import Organization
from main_service.domain.organizations.repositories import OrganizationRepository


class ReadOrganizationUsecase:
    def __init__(self, repository: OrganizationRepository):
        self.__repository = repository

    async def __call__(self, organization_id: int) -> Organization:
        return await self.__repository.read(organization_id)