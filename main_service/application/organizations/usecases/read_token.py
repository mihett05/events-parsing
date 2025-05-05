from uuid import UUID

from domain.organizations.entities import OrganizationToken
from domain.organizations.repositories import OrganizationTokensRepository


class ReadOrganizationTokenUseCase:
    def __init__(self, repository: OrganizationTokensRepository):
        self.__repository = repository

    async def __call__(self, token_id: UUID) -> OrganizationToken:
        return await self.__repository.read(token_id)
