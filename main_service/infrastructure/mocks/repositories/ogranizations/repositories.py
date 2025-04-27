import datetime

from domain.organizations import dtos as dtos
from domain.organizations import entities as entities
from domain.organizations.entities import Organization
from domain.organizations.exceptions import (
    OrganizationAlreadyExistsError,
    OrganizationNotFoundError,
)
from domain.organizations.repositories import OrganizationsRepository
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

    async def create(
        self, organization: entities.Organization
    ) -> entities.Organization:
        organization.id = self.__next_id
        self.__next_id += 1
        organization.created_at = datetime.datetime.utcnow()
        return await self.__repository.create(organization)

    async def read(self, id_: int) -> entities.Organization:
        return await self.__repository.read(id_)

    async def read_all(
        self, dto: dtos.ReadOrganizationsDto
    ) -> list[entities.Organization]:
        data = await self.__repository.read_all()
        return data[dto.page * dto.page_size : (dto.page + 1) * dto.page_size]

    async def update(self, organization: Organization) -> Organization:
        return await self.__repository.update(organization)

    async def delete(self, organization: Organization) -> Organization:
        return await self.__repository.delete(organization)
