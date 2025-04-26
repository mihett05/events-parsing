from domain.events import dtos as dtos
from domain.events import entities as entities
from domain.events.dtos import (
    CreateEventDto,
    ReadAllEventsDto,
    ReadAllEventsFeedDto,
)
from domain.events.entities import Event
from domain.events.exceptions import (
    EventAlreadyExistsError,
    EventNotFoundError,
)
from domain.events.repositories import EventsRepository
from .mappers import map_create_dto_to_entity
from ..crud import Id, MockRepository, MockRepositoryConfig


class EventsMemoryRepository(EventsRepository):
    class Config(MockRepositoryConfig):
        def __init__(self):
            super().__init__(
                entity=Event,
                not_found_exception=EventNotFoundError,
                already_exists_exception=EventAlreadyExistsError,
            )

        def extract_id(self, entity: Event) -> Id:
            return entity.id

    def __init__(self):
        self.__next_id = 1
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
        event = map_create_dto_to_entity(create_dto)

        event.id = self.__next_id
        self.__next_id += 1

        return await self.__repository.create(event)

    async def read(self, event_id: int) -> Event:
        return await self.__repository.read(event_id)

    async def read_all(self, dto: ReadAllEventsDto) -> list[Event]:
        data = await self.__repository.read_all()
        return data

    async def read_for_feed(self, dto: ReadAllEventsFeedDto) -> list[Event]:
        data = await self.__repository.read_all()
        return data[dto.page * dto.page_size : (dto.page + 1) * dto.page_size]

    async def update(self, event: Event) -> Event:
        return await self.__repository.update(event)

    async def delete(self, event: Event) -> Event:
        return await self.__repository.delete(event)
