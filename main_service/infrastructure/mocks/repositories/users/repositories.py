from datetime import datetime

from domain.users import dtos as dtos
from domain.users import entities as entities
from domain.users.entities import User, UserOrganizationRole
from domain.users.enums import RoleEnum
from domain.users.exceptions import UserAlreadyExistsError, UserNotFoundError
from domain.users.repositories import UsersRepository, UserOrganizationRolesRepository
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
        return data[dto.page * dto.page_size: (dto.page + 1) * dto.page_size]

    async def read_by_ids(self, user_ids: list[int]) -> list[entities.User]:
        return [await self.read(user_id) for user_id in user_ids]

    async def update(self, user: User) -> User:
        return await self.__repository.update(user)

    async def delete(self, user: User) -> User:
        return await self.__repository.delete(user)

    async def clear(self):
        await self.__repository.clear()


class UserRolesMemoryRepository(UserOrganizationRolesRepository):

    def __init__(self):
        pass

    async def create(self, role: UserOrganizationRole) -> UserOrganizationRole:
        pass

    async def read(
            self, user_id: int
    ) -> list[UserOrganizationRole]:
        return [UserOrganizationRole(-1, user_id, RoleEnum.SUPER_USER)]

    async def read_all(self, user_id: int) -> list[UserOrganizationRole]:
        pass

    async def update(
            self, user_role: UserOrganizationRole
    ) -> UserOrganizationRole:
        pass

    async def delete(
            self, user_role: UserOrganizationRole
    ) -> UserOrganizationRole:
        pass
