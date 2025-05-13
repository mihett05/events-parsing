from abc import ABCMeta, abstractmethod
from uuid import UUID

from domain.users.dtos import ReadAllUsersDto
from domain.users.entities import User, UserActivationToken, UserOrganizationRole


class UsersRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, user: User) -> User: ...

    @abstractmethod
    async def read(self, user_id: int) -> User: ...

    @abstractmethod
    async def read_by_email(self, email: str) -> User: ...

    @abstractmethod
    async def read_all(self, dto: ReadAllUsersDto) -> list[User]: ...

    @abstractmethod
    async def read_by_ids(
        self,
        user_ids: list[int],
    ) -> list[User]: ...

    @abstractmethod
    async def update(self, user: User) -> User: ...

    @abstractmethod
    async def delete(self, user: User) -> User: ...


class UserOrganizationRolesRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, role: UserOrganizationRole) -> UserOrganizationRole: ...

    @abstractmethod
    async def read(self, user_id: int) -> list[UserOrganizationRole]: ...

    @abstractmethod
    async def update(self, role: UserOrganizationRole) -> UserOrganizationRole: ...

    @abstractmethod
    async def delete(self, role: UserOrganizationRole) -> UserOrganizationRole: ...


class ActivationTokenRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create_activation_token(self, user: User) -> UserActivationToken: ...

    @abstractmethod
    async def read_activation_token(self, token_uuid: UUID) -> UserActivationToken: ...
