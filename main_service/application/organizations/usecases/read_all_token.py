from domain.organizations.dtos import ReadOrganizationTokensDto
from domain.organizations.entities import OrganizationToken
from domain.organizations.repositories import OrganizationTokensRepository


class ReadAllOrganizationTokensUseCase:
    def __init__(self, repository: OrganizationTokensRepository):
        self.__repository = repository

    async def __call__(self, dto: ReadOrganizationTokensDto) -> list[OrganizationToken]:
        return await self.__repository.read_all(dto)
