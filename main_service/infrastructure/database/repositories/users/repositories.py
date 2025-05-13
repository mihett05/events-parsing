from uuid import UUID

import domain.users.dtos as dtos
from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from domain.users import entities as entities
from domain.users.entities import User, UserOrganizationRole, UserActivationToken
from domain.users.exceptions import UserAlreadyExistsError, UserNotFoundError
from domain.users.repositories import (
    UserOrganizationRolesRepository,
    UsersRepository,
)
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.interfaces import LoaderOption

from ..repository import PostgresRepository, PostgresRepositoryConfig
from .mappers import (
    map_from_db,
    map_to_db,
    user_organization_role_map_from_db,
    user_organization_role_map_to_db,
    user_activation_token_map_from_db,
    user_activation_token_map_to_db,
)
from .models import (
    UserDatabaseModel,
    UserOrganizationRoleDatabaseModel,
    UserSettingsDatabaseModel,
    UserActivationTokenDatabaseModel,
)


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

        def get_options(self) -> list[LoaderOption]:
            return [selectinload(self.model.settings)]

    def __init__(self, session: AsyncSession):
        self.__config = self.Config()
        self.__session = session
        self.__repository = PostgresRepository(session, self.__config)

    async def read_all(self, dto: dtos.ReadAllUsersDto) -> list[entities.User]:
        return await self.__repository.read_all(dto)

    async def read_by_ids(self, user_ids: list[int]) -> list[entities.User]:
        return await self.__repository.read_by_ids(user_ids)

    async def create(self, user: User) -> User:
        model: UserDatabaseModel = self.__config.model_mapper(user)
        model.settings = UserSettingsDatabaseModel()
        return await self.__repository.create(model)

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
                not_found_exception=EntityNotFoundError,
                already_exists_exception=EntityAlreadyExistsError,
            )

        def get_select_all_query(self, user_id: int) -> Select:
            return select(self.model).where(self.model.user_id == user_id)

        def extract_id_from_model(self, model: UserOrganizationRoleDatabaseModel):
            return model.organization_id, model.user_id

    def __init__(self, session: AsyncSession):
        self.__config = self.Config()
        self.__session = session
        self.__repository = PostgresRepository(session, self.__config)

    async def create(self, role: UserOrganizationRole) -> UserOrganizationRole:
        return await self.__repository.create_from_entity(role)

    async def read(self, user_id: int) -> list[UserOrganizationRole]:
        return await self.__repository.read_all(user_id)

    async def update(self, role: UserOrganizationRole) -> UserOrganizationRole:
        return await self.__repository.update(role)

    async def delete(self, role: UserOrganizationRole) -> UserOrganizationRole:
        return await self.__repository.delete(role)


class UserActivationTokenDatabaseRepository(UserOrganizationRolesRepository):
    class Config(PostgresRepositoryConfig):
        def __init__(self):
            super().__init__(
                model=UserOrganizationRoleDatabaseModel,
                entity=UserActivationToken,
                entity_mapper=user_activation_token_map_from_db,
                model_mapper=user_activation_token_map_to_db,
                create_model_mapper=None,
                not_found_exception=EntityNotFoundError,
                already_exists_exception=EntityAlreadyExistsError,
            )

        def get_select_all_query(self, token_id: UUID) -> Select:
            return select(self.model).where(self.model.id == token_id)

        def extract_id_from_model(self, model: UserActivationTokenDatabaseModel):
            return model.id

    def __init__(self, session: AsyncSession):
        self.__config = self.Config()
        self.__session = session
        self.__repository = PostgresRepository(session, self.__config)

    async def create(self, token: UserActivationToken) -> UserActivationToken:
        return await self.__repository.create_from_entity(token)

    async def read(self, token_id: UUID) -> UserActivationToken:
        return await self.__repository.read(token_id)

    async def update(self, token: UserActivationToken) -> UserActivationToken:
        return await self.__repository.update(token)

    async def delete(self, token: UserActivationToken) -> UserActivationToken:
        return await self.__repository.delete(token)
