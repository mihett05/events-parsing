from abc import ABCMeta, abstractmethod
from typing import Any

import domain.events.dtos as dtos
import domain.events.entities as entities


class EventsRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, dto: dtos.CreateEventDto) -> entities.Event: ...

    @abstractmethod
    async def find(self, dto: Any) -> entities.Event | None: ...

    @abstractmethod
    async def read(self, event_id: int) -> entities.Event: ...

    @abstractmethod
    async def read_all(self, dto: dtos.ReadAllEventsDto) -> list[entities.Event]: ...

    @abstractmethod
    async def read_for_feed(
        self, dto: dtos.ReadAllEventsFeedDto
    ) -> list[entities.Event]: ...

    @abstractmethod
    async def read_for_user(
        self, dto: dtos.ReadUserEventsDto
    ) -> list[entities.Event]: ...

    @abstractmethod
    async def read_for_organization(
        self, dto: dtos.ReadOrganizationEventsDto
    ) -> list[entities.Event]: ...

    @abstractmethod
    async def update(self, event: entities.Event) -> entities.Event: ...

    @abstractmethod
    async def delete(self, event: entities.Event) -> entities.Event: ...


class EventUsersRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, dto: dtos.CreateEventUserDto) -> entities.EventUser: ...

    @abstractmethod
    async def read(self, event_id: int, user_id: int) -> entities.EventUser: ...

    @abstractmethod
    async def read_for_event(
        self, dto: dtos.ReadEventUsersDto
    ) -> list[entities.EventUser]: ...

    @abstractmethod
    async def delete(self, event_user: entities.EventUser) -> entities.EventUser: ...
