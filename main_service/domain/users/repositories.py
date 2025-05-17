from abc import ABCMeta, abstractmethod
from uuid import UUID

import domain.users.dtos as dtos
import domain.users.entities as entities


class UsersRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, user: entities.User) -> entities.User: ...

    @abstractmethod
    async def read(self, user_id: int) -> entities.User: ...

    @abstractmethod
    async def read_by_email(self, email: str) -> entities.User: ...

    @abstractmethod
    async def read_all(self, dto: dtos.ReadAllUsersDto) -> list[entities.User]: ...

    @abstractmethod
    async def read_by_ids(
        self,
        user_ids: list[int],
    ) -> list[entities.User]: ...

    @abstractmethod
    async def update(self, user: entities.User) -> entities.User: ...

    @abstractmethod
    async def delete(self, user: entities.User) -> entities.User: ...


class UserOrganizationRolesRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(
        self, role: entities.UserOrganizationRole
    ) -> entities.UserOrganizationRole: ...

    @abstractmethod
    async def read(self, user_id: int) -> list[entities.UserOrganizationRole]: ...

    @abstractmethod
    async def update(
        self, role: entities.UserOrganizationRole
    ) -> entities.UserOrganizationRole: ...

    @abstractmethod
    async def delete(
        self, role: entities.UserOrganizationRole
    ) -> entities.UserOrganizationRole: ...


class TelegramTokensRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(
        self, dto: dtos.CreateTelegramTokenDto
    ) -> entities.TelegramToken: ...

    @abstractmethod
    async def read(self, token_id: UUID) -> entities.TelegramToken: ...

    @abstractmethod
    async def update(self, token: entities.TelegramToken) -> entities.TelegramToken: ...
