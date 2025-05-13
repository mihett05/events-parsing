import domain.users.dtos as dtos
from domain.users import entities as entities
from domain.users.entities import User, UserOrganizationRole
from domain.users.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    UserRoleAlreadyExistsError,
    UserRoleNotFoundError,
)
from domain.users.repositories import (
    UserOrganizationRolesRepository,
    UsersRepository,
)
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..repository import PostgresRepository, PostgresRepositoryConfig
from .mappers import (
    map_from_db,
    map_to_db,
    user_organization_role_map_from_db,
    user_organization_role_map_to_db,
)
from .models import UserDatabaseModel, UserOrganizationRoleDatabaseModel


class UsersDatabaseRepository(UsersRepository):
    class Config(PostgresRepositoryConfig):
        def __init__(self):
            super().__init__(
                model=UserDatabaseModel,
                entity=User,
                entity_mapper=map_from_db,
                model_mapper=map_to_db,
                create_model_mapper=None,
                not_found_exception=UserNotFoundError,
                already_exists_exception=UserAlreadyExistsError,
            )

        def get_select_by_email_query(self, email: str) -> Select:
            return select(self.model).where(self.model.email == email)

        def get_select_all_query(self, dto: dtos.ReadAllUsersDto) -> Select:
            return (
                select(self.model)
                .order_by(self.model.id)
                .offset(dto.page * dto.page_size)
                .limit(dto.page_size)
            )

    def __init__(self, session: AsyncSession):
        self.__config = self.Config()
        self.__session = session
        self.__repository = PostgresRepository(session, self.__config)

    async def read_all(self, dto: dtos.ReadAllUsersDto) -> list[entities.User]:
        return await self.__repository.read_all(dto)

    async def create(self, user: User) -> User:
        return await self.__repository.create_from_entity(user)

    async def read(self, user_id: int) -> User:
        return await self.__repository.read(user_id)

    async def read_by_email(self, email: str) -> entities.User:
        if model := await self.__repository.get_scalar_or_none(
            self.__config.get_select_by_email_query(email)
        ):
            return self.__config.model_mapper(model)
        raise self.__config.not_found_exception

    async def update(self, user: User) -> User:
        return await self.__repository.update(user)

    async def delete(self, user: entities.User) -> entities.User:
        return await self.__repository.delete(user)


class UserOrganizationRolesDatabaseRepository(UserOrganizationRolesRepository):
    class Config(PostgresRepositoryConfig):
        def __init__(self):
            super().__init__(
                model=UserOrganizationRoleDatabaseModel,
                entity=UserOrganizationRole,
                entity_mapper=user_organization_role_map_from_db,
                model_mapper=user_organization_role_map_to_db,
                create_model_mapper=None,
                not_found_exception=UserRoleNotFoundError,
                already_exists_exception=UserRoleAlreadyExistsError,
            )

        def get_select_all_query(self, user_id: int) -> Select:
            return select(self.model).where(self.model.user_id == user_id)

        def extract_id_from_entity(self, entity: UserOrganizationRole):
            return {
                "organization_id": entity.organization_id,
                "user_id": entity.user_id,
            }

        def extract_id_from_model(
            self, model: UserOrganizationRoleDatabaseModel
        ):
            return {
                "organization_id": model.organization_id,
                "user_id": model.user_id,
            }

    def __init__(self, session: AsyncSession):
        self.__config = self.Config()
        self.__session = session
        self.__repository = PostgresRepository(session, self.__config)

    async def create(self, role: UserOrganizationRole) -> UserOrganizationRole:
        return await self.__repository.create_from_entity(role)

    async def read_all(self, user_id: int) -> list[UserOrganizationRole]:
        return await self.__repository.read_all(user_id)

    async def read(
        self, user_id: int, organization_id: int
    ) -> UserOrganizationRole:
        return await self.__repository.read(
            {"user_id": user_id, "organization_id": organization_id}
        )

    async def update(self, role: UserOrganizationRole) -> UserOrganizationRole:
        return await self.__repository.update(role)

    async def delete(self, role: UserOrganizationRole) -> UserOrganizationRole:
        return await self.__repository.delete(role)
