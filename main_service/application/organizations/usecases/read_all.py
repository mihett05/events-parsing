from main_service.domain.organizations.repositories import (
    OrganizationRepository,
)
from main_service.domain.organizations.dtos import ReadOrganizationsDto

from main_service.domain.organizations.entities import Organization


class ReadAllOrganizationUseCase:
    def __init__(self, repository: OrganizationRepository):
        self.__repository = repository

    async def __call__(self, dto: ReadOrganizationsDto) -> list[Organization]:
        return await self.__repository.read_all(dto)
