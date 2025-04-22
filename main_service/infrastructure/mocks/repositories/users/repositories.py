from datetime import datetime

from domain.users import dtos as dtos
from domain.users import entities as entities
from domain.users.entities import User
from domain.users.exceptions import UserAlreadyExistsError, UserNotFoundError
from domain.users.repositories import UsersRepository

from ..crud import Id, MockRepository, MockRepositoryConfig


class UsersMemoryRepository(UsersRepository):
    class Config(MockRepositoryConfig):
        def __init__(self):
            super().__init__(
                entity=User,
                not_found_exception=UserNotFoundError,
                already_exists_exception=UserAlreadyExistsError,
            )

        def extract_id(self, entity: User) -> Id:
            return entity.id

    def __init__(self):
        self.__next_id = 1
        self.__repository = MockRepository(self.Config())

    async def read_by_email(self, email: str) -> entities.User:
        for user in await self.__repository.read_all():
            if user.email == email:
                return user
        raise UserNotFoundError()

    async def create(self, user: User) -> entities.User:
        user.id = self.__next_id
        user.created_at = datetime.utcnow()

        self.__next_id += 1
        return await self.__repository.create(user)

    async def read(self, event_id: int) -> User:
        return await self.__repository.read(event_id)

    async def read_all(self, dto: dtos.ReadAllUsersDto) -> list[User]:
        data = await self.__repository.read_all()
        return data[dto.page * dto.page_size : (dto.page + 1) * dto.page_size]

    async def update(self, user: User) -> User:
        return await self.__repository.update(user)

    async def delete(self, user: User) -> User:
        return await self.__repository.delete(user)
