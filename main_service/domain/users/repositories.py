from abc import ABCMeta, abstractmethod

import domain.users.dtos as dtos
import domain.users.entities as entities


class UsersRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, dto: dtos.CreateUserDto) -> entities.User: ...

    @abstractmethod
    async def read(self, user_id: int) -> entities.User: ...

    @abstractmethod
    async def read_all(
        self, dto: dtos.ReadAllUsersDto
    ) -> list[entities.User]: ...

    @abstractmethod
    async def update(self, user: entities.User) -> entities.User: ...

    @abstractmethod
    async def delete(self, user: entities.User) -> entities.User: ...
