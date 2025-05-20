from datetime import datetime
from uuid import UUID

from domain.users import dtos as dtos
from domain.users import entities as entities
from domain.users.entities import TelegramToken, User
from domain.users.exceptions import (
    TelegramTokenAlreadyExistsError,
    TelegramTokenNotFoundError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from domain.users.repositories import TelegramTokensRepository, UsersRepository
from domain.users.entities import User, UserOrganizationRole
from domain.users.exceptions import UserAlreadyExistsError, UserNotFoundError
from domain.users.repositories import UsersRepository, UserOrganizationRolesRepository
from domain.users.entities import User, UserActivationToken, UserOrganizationRole
from domain.users.enums import RoleEnum
from domain.users.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    UserRoleAlreadyExistsError,
    UserRoleNotFoundError,
)
from domain.users.repositories import (
    UserActivationTokenRepository,
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

    async def read_by_email(self, email: str) -> User:
        for user in await self.__repository.read_all():
            if user.email == email:
                return user
        raise UserNotFoundError()

    async def create(self, user: User) -> User:
        user.id = self.__next_id
        user.created_at = datetime.now()

        self.__next_id += 1
        return await self.__repository.create(user)

    async def read(self, user_id: int) -> User:
        return await self.__repository.read(user_id)

    async def read_all(self, dto: dtos.ReadAllUsersDto) -> list[User]:
        data = await self.__repository.read_all()
        return data[dto.page * dto.page_size: (dto.page + 1) * dto.page_size]

    async def read_by_ids(self, user_ids: list[int]) -> list[User]:
        return [await self.read(user_id) for user_id in user_ids]

    async def update(self, user: User) -> User:
        return await self.__repository.update(user)

    async def delete(self, user: User) -> User:
        return await self.__repository.delete(user)


class TelegramTokensMemoryRepository(TelegramTokensRepository):
    class Config(MockRepositoryConfig):
        def __init__(self):
            super().__init__(
                entity=TelegramToken,
                not_found_exception=TelegramTokenNotFoundError,
                already_exists_exception=TelegramTokenAlreadyExistsError,
    
    async def create(self, dto: dtos.CreateTelegramTokenDto) -> TelegramToken:
        token = TelegramToken(id=dto.id, user_id=dto.user_id, created_at=datetime.now())
        return await self.__repository.create(token)

    async def read(self, token_id: UUID) -> TelegramToken:
        return await self.__repository.read(token_id)

    async def update(self, token: TelegramToken) -> TelegramToken:
        return await self.__repository.update(token)
              
    async def clear(self):
        await self.__repository.clear()


class UserOrganizationsRolesMemoryRepository(UserOrganizationRolesRepository):
    class Config(MockRepositoryConfig):
        def __init__(self):
            super().__init__(
                entity=UserOrganizationRole,
                not_found_exception=UserRoleNotFoundError,
                already_exists_exception=UserRoleAlreadyExistsError,
            )

    def __init__(self):
        self.__repository = MockRepository(self.Config())

    async def create(self, role: UserOrganizationRole) -> UserOrganizationRole:
        return await self.__repository.create(role)

    async def read(self, user_id: int) -> list[UserOrganizationRole]:
        return await self.__repository.read(user_id)

    async def update(self, user_role: UserOrganizationRole) -> UserOrganizationRole:
        return await self.__repository.update(user_role)
      
    async def update_is_active_statement(self, user: User, status: bool):
        user.is_active = status
        await self.__repository.update(user)

    async def delete(self, user_role: UserOrganizationRole) -> UserOrganizationRole:
        return await self.__repository.delete(user_role)
    
    async def clear(self):
        await self.__repository.clear()


class UserActivationTokenMemoryRepository(UserActivationTokenRepository):
    class Config(MockRepositoryConfig):
        def __init__(self):
            super().__init__(
                entity=UserActivationToken,
                not_found_exception=UserNotFoundError,
                already_exists_exception=UserAlreadyExistsError,
            )

    def __init__(self):
        self.__repository = MockRepository(self.Config())

    async def read(self, token_uuid: UUID) -> UserActivationToken:
        return await self.__repository.read(token_uuid)

    async def create(self, token: UserActivationToken) -> UserActivationToken:
        return await self.__repository.create(token)

    async def update_is_used_statement(self, token: UserActivationToken):
        token.is_used = True
        await self.__repository.update(token)

    async def delete(self, token: UserActivationToken) -> UserActivationToken:
        return await self.__repository.delete(token)
    
    async def clear(self):
        await self.__repository.clear()
