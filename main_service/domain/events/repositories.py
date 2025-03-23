from abc import ABCMeta, abstractmethod

import domain.events.dtos as dtos
import domain.events.entities as entities


class EventsRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, dto: dtos.CreateEventDto) -> entities.Event: ...

    @abstractmethod
    async def read(self, id_: int) -> entities.Event: ...

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
