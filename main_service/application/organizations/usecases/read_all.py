from typing import List

from main_service.domain.organizations.repositories import (
    OrganizationRepository,
)
from main_service.domain.organizations.dtos import ReadOrganizationsDto

from main_service.domain.organizations.entities import Organization


class ReadAllOrganizationUsecase:
    def __init__(self, repository: OrganizationRepository):
        self.__repository = repository

    async def __call__(self, dto: ReadOrganizationsDto) -> List[Organization]:
        return await self.__repository.read_all(dto)
