from sqlalchemy import Select, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

import domain.events.dtos as dtos
from domain.events.entities import Event
from domain.events.exceptions import (
    EventAlreadyExistsError,
    EventNotFoundError,
)
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
                not_found_exception=EventNotFoundError,
                already_exists_exception=EventAlreadyExistsError,
            )

        def get_select_all_query(self, dto: dtos.ReadAllEventsDto) -> Select:
            query = select(self.model).order_by(self.model.id)
            query = self.__try_add_period_filter_to_query(query, dto)
            return query

        def get_select_all_feed_query(
            self, dto: dtos.ReadAllEventsFeedDto
        ) -> Select:
            query = select(self.model).order_by(self.model.id)

            query = self.__try_add_period_filter_to_query(query, dto)
            query = self.__try_add_organization_filter_to_query(query, dto)
            query = self.__add_offset_to_query(query, dto)
            return query

        def __try_add_period_filter_to_query(
            self, query, dto: dtos.ReadAllEventsFeedDto | dtos.ReadAllEventsDto
        ) -> Select:
            if dto.start_date is None and dto.end_date is None:
                return query

            conditions = []
            if dto.start_date is not None:
                if self.model.end_date is None:
                    conditions.append(dto.start_date <= self.model.start_date)
                else:
                    conditions.append(dto.start_date <= self.model.end_date)
            if dto.end_date is not None:
                conditions.append(self.model.start_date <= dto.end_date)
            return query.where(and_(*conditions))

        def __try_add_organization_filter_to_query(
            self, query, dto: dtos.ReadAllEventsFeedDto
        ) -> Select:
            if dto.organization_id is None:
                return query
            return query.where(
                self.model.organization_id == dto.organization_id
            )

        def __add_offset_to_query(
            self, query, dto: dtos.ReadAllEventsFeedDto
        ) -> Select:
            return query.offset(dto.page * dto.page_size).limit(dto.page_size)

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
        query = self.config.get_select_all_query(dto)
        return await self.__repository.get_entities_from_query(query)

    async def read_for_feed(
        self, dto: dtos.ReadAllEventsFeedDto
    ) -> list[Event]:
        query = self.config.get_select_all_feed_query(dto)
        return await self.__repository.get_entities_from_query(query)

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
