from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import LoaderOption

import domain.events.dtos as dtos
from application.events.dtos import EventInfo
from domain.events.entities import Event
from domain.events.exceptions import EventNotFound, EventAlreadyExists
from domain.events.repositories import EventsRepository
from .mappers import map_from_db, map_to_db
from .models import EventDatabaseModel
from ..repository import PostgresRepositoryConfig, PostgresRepository, Id


class EventsDatabaseRepository(EventsRepository):
    class Config(PostgresRepositoryConfig):
        def __init__(self):
            super().__init__(
                model=EventDatabaseModel,
                entity=Event,
                entity_mapper=map_from_db,
                model_mapper=map_to_db,
                not_found_exception=EventNotFound,
                already_exists_exception=EventAlreadyExists,
            )

        def extract_id_from_entity(self, entity: Event) -> Id:
            return entity.id

        def extract_id_from_model(self, model: EventDatabaseModel) -> Id:
            return model.id

        def get_options(self) -> list[LoaderOption]:
            return []

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

    async def find(self, event_info: EventInfo) -> Event | None:
        query = select(EventDatabaseModel).where(
            EventDatabaseModel.title.ilike(event_info.title),
            EventDatabaseModel.end_date == event_info.dates.end_date,
            EventDatabaseModel.start_date == event_info.dates.start_date,
            EventDatabaseModel.end_registration
            == event_info.dates.end_registration,
        )
        model: (
            EventDatabaseModel | None
        ) = await self.__repository.run_query_and_get_scalar_or_none(query)
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
        event = Event(
            title=dto.title,
            description=dto.description,
            end_date=dto.end_date,
            start_date=dto.start_date,
            end_registration=dto.end_registration,
        )
        return await self.__repository.create(event)

    async def update(self, event: Event) -> Event:
        return await self.__repository.update(event)

    async def delete(self, event: Event) -> Event:
        return await self.__repository.delete(event)
