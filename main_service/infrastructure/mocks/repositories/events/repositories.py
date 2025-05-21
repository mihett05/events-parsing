from datetime import timedelta

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

from ..crud import Id, MockRepository, MockRepositoryConfig
from .mappers import map_create_dto_to_entity


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
        res = []
        for event in data:
            if (
                dto.start_date
                <= event.start_date
                <= dto.start_date + timedelta(days=1)
            ):
                res.append(event)
        return res

    async def read_for_feed(self, dto: ReadAllEventsFeedDto) -> list[Event]:
        data = await self.__repository.read_all()
        res = []
        for event in data:
            start = (
                dto.start_date is None
                or dto.start_date <= event.start_date
                or dto.start_date <= event.end_date
            )
            end = dto.end_date is None or event.start_date <= dto.end_date
            organization = (
                dto.organization_id is None
                or event.organization_id == dto.organization_id
            )
            type_ = dto.type is None or event.type == dto.type
            format_ = dto.format is None or event.format == dto.format
            if start and end and organization and type_ and format_:
                res.append(event)
        return res[dto.page * dto.page_size : (dto.page + 1) * dto.page_size]

    async def update(self, event: Event) -> Event:
        return await self.__repository.update(event)

    async def delete(self, event: Event) -> Event:
        return await self.__repository.delete(event)
