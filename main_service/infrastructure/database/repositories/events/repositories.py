import domain.events.dtos as dtos
from domain.events import entities as entities
from domain.events.entities import Event, EventUser
from domain.events.exceptions import (
    EventAlreadyExistsError,
    EventNotFoundError,
    EventUserAlreadyExistsError,
    EventUserNotFoundError,
)
from domain.events.repositories import EventsRepository, EventUsersRepository
from sqlalchemy import Select, and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.interfaces import LoaderOption

from ..repository import PostgresRepository, PostgresRepositoryConfig
from ..users import UserDatabaseModel
from .mappers import (
    event_user_map_from_db,
    event_user_map_to_db,
    map_create_dto_to_model,
    map_from_db,
    map_to_db,
)
from .models import EventDatabaseModel, EventUserDatabaseModel


class EventsUserDatabaseRepository(EventUsersRepository):
    class Config(PostgresRepositoryConfig):
        def __init__(self):
            super().__init__(
                model=EventUserDatabaseModel,
                entity=EventUser,
                entity_mapper=event_user_map_from_db,
                model_mapper=event_user_map_to_db,
                create_model_mapper=None,
                not_found_exception=EventUserNotFoundError,
                already_exists_exception=EventUserAlreadyExistsError,
            )

        def get_select_for_user(self, dto: dtos.ReadUserEventsDto) -> Select:
            query = select(self.model).where(self.model.user_id == dto.user_id)
            return self.__add_offset_to_query(query, dto)

        def get_select_for_event(self, dto: dtos.ReadEventUsersDto) -> Select:
            query = select(self.model).where(self.model.event_id == dto.event_id)
            return self.__add_offset_to_query(query, dto)

        def extract_id_from_model(self, model: EventUserDatabaseModel):
            return model.event_id, model.user_id

        def extract_id_from_entity(self, event_user: EventUser):
            return event_user.event_id, event_user.user_id

        def __add_offset_to_query(
            self, query, dto: dtos.ReadEventUsersDto | dtos.ReadUserEventsDto
        ) -> Select:
            return query.offset(dto.page * dto.page_size).limit(dto.page_size)

    def __init__(self, session: AsyncSession):
        self.session = session
        self.config = self.Config()
        self.__repository = PostgresRepository(session, self.config)

    async def create(self, event_user: EventUser) -> entities.EventUser:
        return await self.__repository.create_from_entity(event_user)

    async def read_for_user(
        self, dto: dtos.ReadUserEventsDto
    ) -> list[entities.EventUser]:
        query = self.config.get_select_for_user(dto)
        return await self.__repository.get_entities_from_query(query)

    async def read_for_event(
        self, dto: dtos.ReadEventUsersDto
    ) -> list[entities.EventUser]:
        query = self.config.get_select_for_event(dto)
        return await self.__repository.get_entities_from_query(query)

    async def delete(self, event_user: EventUser) -> entities.EventUser:
        return await self.__repository.delete(event_user)


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
            query = (
                select(self.model)
                .order_by(self.model.id)
                .where(self.model.start_date == dto.start_date)
            )
            if dto.for_update:
                query = query.with_for_update(skip_locked=True)

            return query

        def get_select_all_feed_query(self, dto: dtos.ReadAllEventsFeedDto) -> Select:
            query = select(self.model).order_by(desc(self.model.start_date))

            query = self.__try_add_period_filter_to_query(query, dto)
            query = self.__try_add_organization_filter_to_query(query, dto)
            query = self.__try_add_type_filter_to_query(query, dto)
            query = self.__try_add_format_filter_to_query(query, dto)
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
            return query.where(self.model.organization_id == dto.organization_id)

        def __try_add_type_filter_to_query(
            self, query, dto: dtos.ReadAllEventsFeedDto
        ) -> Select:
            if dto.type is None:
                return query
            return query.where(self.model.type == dto.type)

        def __try_add_format_filter_to_query(
            self, query, dto: dtos.ReadAllEventsFeedDto
        ) -> Select:
            if dto.format is None:
                return query
            return query.where(self.model.format == dto.format)

        def __add_offset_to_query(
            self, query, dto: dtos.ReadAllEventsFeedDto | dtos.ReadUserEventsDto
        ) -> Select:
            return query.offset(dto.page * dto.page_size).limit(dto.page_size)

        def get_options_with_members(self) -> list[LoaderOption]:
            return [
                joinedload(self.model.attachments),
                joinedload(self.model.members).joinedload(UserDatabaseModel.settings),
            ]

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
        model = (
            (await self.__session.execute(self.config.add_options(query)))
            .unique()
            .scalar_one_or_none()
        )
        return model and self.config.entity_mapper(model)

    async def read(self, event_id: int) -> Event:
        if model := await self.__session.get(
            self.config.model,
            event_id,
            options=self.config.get_options_with_members(),
            populate_existing=True,
        ):
            return self.config.entity_mapper(model, True)
        raise self.config.not_found_exception()

    async def read_all(self, dto: dtos.ReadAllEventsDto) -> list[Event]:
        query = self.config.get_select_all_query(dto)
        return await self.__repository.get_entities_from_query(query)

    async def read_for_feed(self, dto: dtos.ReadAllEventsFeedDto) -> list[Event]:
        query = self.config.get_select_all_feed_query(dto)
        return await self.__repository.get_entities_from_query(query)

    async def read_for_user(self, dto: dtos.ReadUserEventsDto) -> list[Event]:
        raise NotImplementedError("Method is unavailable for now")
        # query = self.config.get_select_for_user_query(dto)
        # return await self.__repository.get_entities_from_query(query)

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
