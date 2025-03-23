from abc import ABCMeta, abstractmethod

import MainService.Domain.User.Entities as ent
import MainService.Domain.User.Dtos as dtos


class UserRepository(metaclass= ABCMeta):
    @abstractmethod
    async def create(self, dto: dtos.CreateUserDto) -> ent.User: ...
    @abstractmethod
    async def read(self, id_: int) -> ent.User: ...
    @abstractmethod
    async def read_all(self, dto: dtos.ReadUsersDto) -> list[ent.User]: ...
    @abstractmethod
    async def update(self, user: ent.User) -> ent.User: ...
    @abstractmethod
    async def delete(self, user: ent.User) -> ent.User: ...