from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.organizations import dtos
from domain.organizations.entities import Organization
from domain.organizations.exceptions import (
    OrganizationAlreadyExistsError,
    OrganizationNotFoundError,
)
from domain.organizations.repositories import OrganizationsRepository
from infrastructure.database.repositories.organizations.models import (
    OrganizationDatabaseModel,
)

from ..repository import PostgresRepository, PostgresRepositoryConfig
from .mappers import map_create_dto_to_model, map_from_db, map_to_db


class OrganizationsDatabaseRepository(OrganizationsRepository):
    class Config(PostgresRepositoryConfig):
        def __init__(self):
            super().__init__(
                model=OrganizationDatabaseModel,
                entity=Organization,
                entity_mapper=map_from_db,
                model_mapper=map_to_db,
                create_model_mapper=map_create_dto_to_model,
                not_found_exception=OrganizationNotFoundError,
                already_exists_exception=OrganizationAlreadyExistsError,
            )

        def get_select_all_query(
            self, dto: dtos.ReadOrganizationsDto
        ) -> Select:
            return (
                select(self.model)
                .order_by(self.model.id)
                .offset(dto.page * dto.page_size)
                .limit(dto.page_size)
            )

    def __init__(self, session: AsyncSession):
        self.__session = session
        self.__config = self.Config()
        self.__repository = PostgresRepository(session, self.__config)

    async def read(self, organization_id: int) -> Organization:
        return await self.__repository.read(organization_id)

    async def read_all(
        self, dto: dtos.ReadOrganizationsDto
    ) -> list[Organization]:
        return await self.__repository.read_all(dto)

    async def create(self, dto: dtos.CreateOrganizationDto) -> Organization:
        return await self.__repository.create_from_dto(dto)

    async def update(self, organization: Organization) -> Organization:
        return await self.__repository.update(organization)

    async def delete(self, organization: Organization) -> Organization:
        return await self.__repository.delete(organization)
