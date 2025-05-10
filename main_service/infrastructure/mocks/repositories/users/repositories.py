from datetime import datetime

from domain.users import dtos as dtos
from domain.users import entities as entities
from domain.users.entities import User, UserOrganizationRole
from domain.users.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
from domain.users.repositories import (
    UserOrganizationRolesRepository,
    UsersRepository,
)

from ..crud import MockRepository, MockRepositoryConfig


class UsersMemoryRepository(UsersRepository):
    class Config(MockRepositoryConfig):
        def __init__(self):
            super().__init__(
                entity=User,
                not_found_exception=UserNotFoundError,
                already_exists_exception=UserAlreadyExistsError,
            )

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
        user.created_at = datetime.now()

        self.__next_id += 1
        return await self.__repository.create(user)

    async def read(self, user_id: int) -> User:
        return await self.__repository.read(user_id)

    async def read_all(self, dto: dtos.ReadAllUsersDto) -> list[User]:
        data = await self.__repository.read_all()
        return data[dto.page * dto.page_size : (dto.page + 1) * dto.page_size]

    async def read_by_ids(self, user_ids: list[int]) -> list[entities.User]:
        return [await self.read(user_id) for user_id in user_ids]

    async def update(self, user: User) -> User:
        return await self.__repository.update(user)

    async def delete(self, user: User) -> User:
        return await self.__repository.delete(user)


class UserOrganizationRolesMemoryRepository(UserOrganizationRolesRepository):
    storage: dict[int, list[UserOrganizationRole]]
    __config: MockRepositoryConfig

    def __init__(self, config: MockRepositoryConfig):
        self.storage = dict()
        self.__config = config

    async def create(self, role: UserOrganizationRole) -> UserOrganizationRole:
        if role.user_id in self.storage:
            raise self.__config.already_exists_exception()

        self.storage[role.user_id].append(role)
        return role

    async def read(
        self, user_id: int, organization_id: int
    ) -> UserOrganizationRole:
        if user_id not in self.storage:
            raise self.__config.not_found_exception()
        for role in self.storage[user_id]:
            if role.organization_id == organization_id:
                return role
        raise self.__config.not_found_exception()

    async def read_all(self, user_id: int) -> list[UserOrganizationRole]:
        if user_id not in self.storage:
            raise self.__config.not_found_exception()
        return self.storage[user_id]

    async def update(
        self, user_role: UserOrganizationRole
    ) -> UserOrganizationRole:
        if user_role.user_id not in self.storage:
            raise self.__config.not_found_exception()
        for role in self.storage[user_role.user_id]:
            if role.organization_id == user_role.organization_id:
                role = user_role
                return role
        raise self.__config.not_found_exception()

    async def delete(
        self, user_role: UserOrganizationRole
    ) -> UserOrganizationRole:
        if user_role.user_id not in self.storage:
            raise self.__config.not_found_exception()
        role_storage_index = None
        for index, role in enumerate(self.storage[user_role.user_id]):
            if role.organization_id == user_role.organization_id:
                role_storage_index = index
                break
        if role_storage_index:
            deleted_role = self.storage[user_role.user_id][role_storage_index]
            self.storage[user_role.user_id].pop(role_storage_index)
            return deleted_role
        raise self.__config.not_found_exception()
