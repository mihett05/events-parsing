from domain.events import dtos as dtos
from domain.events import entities as entities
from domain.events.dtos import CreateEventDto
from domain.events.entities import Event
from domain.events.exceptions import (
    EventAlreadyExistsErrorError,
    EventNotFoundErrorError,
)
from domain.events.repositories import EventsRepository

from ..crud import Id, MockRepository, MockRepositoryConfig
from .mappers import map_create_dto_to_entity


class EventsMemoryRepository(EventsRepository):
    class Config(MockRepositoryConfig):
        def __init__(self):
            super().__init__(
                entity=Event,
                not_found_exception=EventNotFoundErrorError,
                already_exists_exception=EventAlreadyExistsErrorError,
            )

        def extract_id(self, entity: Event) -> Id:
            return entity.id

    def __init__(self):
        self.__repository = MockRepository(self.Config())

    async def find(self, dto: dtos.CreateEventDto) -> entities.Event | None:
        for entity in await self.__repository.read_all():
            if (
                entity.title.lower() == dto.title.lower()
                and entity.end_date == dto.end_date
                and entity.start_date == dto.start_date
                and entity.end_registration == dto.end_registration
            ):
                return entity
        return None

    async def read_for_user(
        self, dto: dtos.ReadUserEventsDto
    ) -> list[entities.Event]:
        raise NotImplementedError

    async def read_for_organization(
        self, dto: dtos.ReadOrganizationEventsDto
    ) -> list[entities.Event]:
        raise NotImplementedError

    async def create(self, create_dto: CreateEventDto) -> Event:
        return await self.__repository.create(
            map_create_dto_to_entity(create_dto)
        )

    async def read(self, event_id: int) -> Event:
        return await self.__repository.read(event_id)

    async def read_all(self, event_ids: list[int]) -> list[Event]:
        return [
            await self.__repository.read(event_id) for event_id in event_ids
        ]

    async def update(self, event: Event) -> Event:
        return await self.__repository.update(event)

    async def delete(self, event: Event) -> Event:
        return await self.__repository.delete(event)
