import datetime
from uuid import UUID

from domain.organizations import dtos as dtos
from domain.organizations import entities as entities
from domain.organizations.dtos import (
    CreateOrganizationTokenDto,
    ReadOrganizationTokensDto,
)
from domain.organizations.entities import Organization, OrganizationToken
from domain.organizations.exceptions import (
    OrganizationAlreadyExistsError,
    OrganizationNotFoundError,
    OrganizationTokenAlreadyExistsError,
    OrganizationTokenNotFoundError,
)
from domain.organizations.repositories import (
    OrganizationsRepository,
    OrganizationTokensRepository,
)

from infrastructure.mocks.repositories.crud import (
    MockRepository,
    MockRepositoryConfig,
)


class OrganizationsMemoryRepository(OrganizationsRepository):
    class Config(MockRepositoryConfig):
        def __init__(self):
            super().__init__(
                entity=Organization,
                not_found_exception=OrganizationNotFoundError,
                already_exists_exception=OrganizationAlreadyExistsError,
            )

    def __init__(self):
        self.__next_id = 1
        self.__repository = MockRepository(self.Config())

    async def create(self, dto: dtos.CreateOrganizationDto) -> entities.Organization:
        organization = entities.Organization(
            title=dto.title,
            owner_id=dto.owner_id,
            id=self.__next_id,
            created_at=datetime.datetime.now(datetime.UTC),
        )
        self.__next_id += 1
        return await self.__repository.create(organization)

    async def read(self, id_: int) -> entities.Organization:
        return await self.__repository.read(id_)

    async def find(self, owner_id: int) -> entities.Organization | None:
        for org in await self.__repository.read_all():
            if org.owner_id == owner_id:
                return org

    async def read_all(
        self, dto: dtos.ReadOrganizationsDto
    ) -> list[entities.Organization]:
        data = await self.__repository.read_all()
        return data[dto.page * dto.page_size : (dto.page + 1) * dto.page_size]

    async def update(self, organization: Organization) -> Organization:
        return await self.__repository.update(organization)

    async def delete(self, organization: Organization) -> Organization:
        return await self.__repository.delete(organization)

    async def clear(self):
        await self.__repository.clear()


class OrganizationTokensMemoryRepository(OrganizationTokensRepository):
    class Config(MockRepositoryConfig):
        def __init__(self):
            super().__init__(
                entity=OrganizationToken,
                not_found_exception=OrganizationTokenNotFoundError,
                already_exists_exception=OrganizationTokenAlreadyExistsError,
            )

    def __init__(self):
        self.__repository = MockRepository(self.Config())

    async def create(self, dto: CreateOrganizationTokenDto) -> OrganizationToken:
        token = OrganizationToken(id=dto.id, created_by=dto.created_by)
        return await self.__repository.create(token)

    async def read(self, token_id: UUID) -> OrganizationToken:
        return await self.__repository.read(token_id)

    async def update(self, token: OrganizationToken) -> OrganizationToken:
        return await self.__repository.update(token)

    async def delete(self, token: OrganizationToken) -> OrganizationToken:
        return await self.__repository.delete(token)

    async def read_all(self, dto: ReadOrganizationTokensDto) -> list[OrganizationToken]:
        data = await self.__repository.read_all()
        result = []
        for token in data:
            if token.created_by == dto.created_by:
                result.append(token)
        return result[dto.page * dto.page_size : (dto.page + 1) * dto.page_size]
