from uuid import UUID

from domain.organizations import dtos
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
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.repositories.organizations.models import (
    OrganizationDatabaseModel,
    OrganizationTokenDatabaseModel,
)

from ..repository import PostgresRepository, PostgresRepositoryConfig
from .mappers import (
    map_create_dto_to_model,
    map_from_db,
    map_to_db,
    organization_token_map_create_to_model,
    organization_token_map_from_db,
    organization_token_map_to_db,
)


class OrganizationsDatabaseRepository(OrganizationsRepository):
    """Репозиторий для работы с организациями в базе данных."""

    class Config(PostgresRepositoryConfig):
        """Конфигурация репозитория организаций."""

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

        def get_select_all_query(self, dto: dtos.ReadOrganizationsDto) -> Select:
            """Формирует базовый запрос для получения списка организаций."""

            query = select(self.model).order_by(self.model.id)
            return self.__try_add_pagination(query, dto)

        def __try_add_pagination(
            self, query: Select, dto: dtos.ReadOrganizationsDto
        ) -> Select:
            """Добавляет пагинацию к запросу, если указаны параметры страницы."""

            if dto.page is None or dto.page_size is None:
                return query
            return query.offset(dto.page * dto.page_size).limit(dto.page_size)

    def __init__(self, session: AsyncSession):
        """Инициализирует репозиторий с асинхронной сессией БД."""

        self.__session = session
        self.__config = self.Config()
        self.__repository = PostgresRepository(session, self.__config)

    async def read(self, organization_id: int) -> Organization:
        """Получает организацию по ID."""

        return await self.__repository.read(organization_id)

    async def find(self, owner_id: int) -> Organization | None:
        """Находит организацию по ID владельца."""

        query = select(self.__config.model).where(
            self.__config.model.owner_id == owner_id
        )
        return await self.__repository.get_scalar_or_none(query)

    async def read_all(self, dto: dtos.ReadOrganizationsDto) -> list[Organization]:
        """Возвращает список организаций с возможностью пагинации."""

        return await self.__repository.read_all(dto)

    async def create(self, dto: dtos.CreateOrganizationDto) -> Organization:
        """Создает новую организацию в БД."""

        return await self.__repository.create_from_dto(dto)

    async def update(self, organization: Organization) -> Organization:
        """Обновляет данные организации в БД."""

        return await self.__repository.update(organization)

    async def delete(self, organization: Organization) -> Organization:
        """Удаляет организацию из БД."""

        return await self.__repository.delete(organization)


class OrganizationTokensDatabaseRepository(OrganizationTokensRepository):
    """Репозиторий для работы с токенами организаций в базе данных."""

    class Config(PostgresRepositoryConfig):
        """Конфигурация репозитория токенов организаций."""

        def __init__(self):
            super().__init__(
                model=OrganizationTokenDatabaseModel,
                entity=OrganizationToken,
                entity_mapper=organization_token_map_from_db,
                model_mapper=organization_token_map_to_db,
                create_model_mapper=organization_token_map_create_to_model,
                not_found_exception=OrganizationTokenNotFoundError,
                already_exists_exception=OrganizationTokenAlreadyExistsError,
            )

        def get_select_all_query(self, dto: ReadOrganizationTokensDto) -> Select:
            query = (
                select(self.model)
                .where(self.model.created_by == dto.created_by)
                .order_by(self.model.id)
            )
            return self.__add_offset_to_query(query, dto)

        def __add_offset_to_query(
            self, query, dto: ReadOrganizationTokensDto
        ) -> Select:
            return query.offset(dto.page * dto.page_size).limit(dto.page_size)

    def __init__(self, session: AsyncSession):
        self.__session = session
        self.__config = self.Config()
        self.__repository = PostgresRepository(session, self.__config)

    async def read(self, token_id: UUID) -> OrganizationToken:
        return await self.__repository.read(token_id)

    async def create(self, dto: CreateOrganizationTokenDto) -> OrganizationToken:
        return await self.__repository.create_from_dto(dto)

    async def update(self, token: OrganizationToken) -> OrganizationToken:
        return await self.__repository.update(token)

    async def delete(self, token: OrganizationToken) -> OrganizationToken:
        return await self.__repository.delete(token)

    async def read_all(self, dto: ReadOrganizationTokensDto) -> list[OrganizationToken]:
        return await self.__repository.read_all(dto)
