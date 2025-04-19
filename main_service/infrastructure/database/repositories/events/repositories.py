from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

import domain.events.dtos as dtos
from domain.events.entities import Event
from domain.events.exceptions import EventAlreadyExists, EventNotFound
from domain.events.repositories import EventsRepository

from ..repository import PostgresRepository, PostgresRepositoryConfig
from .mappers import map_create_dto_to_model, map_from_db, map_to_db
from .models import EventDatabaseModel


class EventsDatabaseRepository(EventsRepository):
    class Config(PostgresRepositoryConfig):
        def __init__(self):
            super().__init__(
                model=EventDatabaseModel,
                entity=Event,
                entity_mapper=map_from_db,
                model_mapper=map_to_db,
                create_model_mapper=map_create_dto_to_model,
                not_found_exception=EventNotFound,
                already_exists_exception=EventAlreadyExists,
            )

        def get_select_all_query(self, dto: dtos.ReadAllEventsDto) -> Select:
            return (
                select(self.model)
                .order_by(self.model.id)
                .offset(dto.page * dto.page_size)
                .limit(dto.page_size)
            )

    def __init__(self, session: AsyncSession):
        self.__session = session
        self.config = self.Config()
        self.__repository = PostgresRepository(session, self.config)

    async def find(self, event_info: dtos.CreateEventDto) -> Event | None:
        query = select(EventDatabaseModel).where(
            EventDatabaseModel.title.ilike(event_info.title),
            EventDatabaseModel.end_date == event_info.end_date,
            EventDatabaseModel.start_date == event_info.start_date,
            EventDatabaseModel.end_registration == event_info.end_registration,
        )
        model: (
            EventDatabaseModel | None
        ) = await self.__repository.get_scalar_or_none(query)
        return model and self.config.entity_mapper(model)

    async def read(self, event_id: int) -> Event:
        return await self.__repository.read(event_id)

    async def read_all(self, dto: dtos.ReadAllEventsDto) -> list[Event]:
        return await self.__repository.read_all(dto)

    async def read_for_user(self, dto: dtos.ReadUserEventsDto) -> list[Event]:
        raise NotImplementedError("Method is unavailable for now")

    async def read_for_organization(
        self, dto: dtos.ReadOrganizationEventsDto
    ) -> list[Event]:
        raise NotImplementedError("Method is unavailable for now")

    async def create(self, dto: dtos.CreateEventDto) -> Event:
        return await self.__repository.create_from_dto(dto)

    async def update(self, event: Event) -> Event:
        return await self.__repository.update(event)

    async def delete(self, event: Event) -> Event:
        return await self.__repository.delete(event)
