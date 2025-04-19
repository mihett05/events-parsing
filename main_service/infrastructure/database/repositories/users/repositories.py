from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

import domain.users.dtos as dtos
from domain.users import entities as entities
from domain.users.entities import User
from domain.users.exceptions import UserAlreadyExists, UserNotFound
from domain.users.repositories import UsersRepository

from ..repository import PostgresRepository, PostgresRepositoryConfig
from .mappers import map_from_db, map_to_db
from .models import UserDatabaseModel


class UsersDatabaseRepository(UsersRepository):
    class Config(PostgresRepositoryConfig):
        def __init__(self):
            super().__init__(
                model=UserDatabaseModel,
                entity=User,
                entity_mapper=map_from_db,
                model_mapper=map_to_db,
                create_model_mapper=None,
                not_found_exception=UserNotFound,
                already_exists_exception=UserAlreadyExists,
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
