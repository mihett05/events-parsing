from datetime import datetime, timedelta

import application.events.usecases as usecases
import pytest_asyncio
from application.events.dtos import UpdateEventDto
from dishka import AsyncContainer
from domain.events.dtos import (
    CreateEventDto,
    ReadAllEventsDto,
    ReadOrganizationEventsDto,
    ReadUserEventsDto,
)
from domain.events.entities import Event
from domain.events.repositories import EventsRepository


@pytest_asyncio.fixture
async def create_event_dto() -> CreateEventDto:
    date = datetime.now().date()
    return CreateEventDto(
        title="Example",
        type="Hackathon",
        format="offline",
        location=None,
        description="Example Description",
        end_date=datetime.combine(date, datetime.min.time())
        + timedelta(days=1),
        start_date=datetime.combine(date, datetime.min.time()),
        end_registration=datetime.combine(date, datetime.min.time())
        - timedelta(days=1),
    )


@pytest_asyncio.fixture
async def update_event_dto() -> UpdateEventDto:
    return UpdateEventDto(
        event_id=1, title="Example New", description="Example Description New"
    )


@pytest_asyncio.fixture
async def read_all_event_dto() -> ReadAllEventsDto:
    return ReadAllEventsDto(
        page=0,
        page_size=50,
    )


@pytest_asyncio.fixture
async def read_organization_events_dto() -> ReadOrganizationEventsDto:
    return ReadOrganizationEventsDto(
        organization_id=1,
        page=0,
        page_size=50,
    )


@pytest_asyncio.fixture
async def read_user_events_dto() -> ReadUserEventsDto:
    return ReadUserEventsDto(
        user_id=1,
        page=0,
        page_size=50,
    )


@pytest_asyncio.fixture
async def event_repository(container: AsyncContainer) -> EventsRepository:
    async with container() as nested:
        yield await nested.get(EventsRepository)


@pytest_asyncio.fixture
async def create_event(
    create_event_dto: CreateEventDto,
    event_repository: EventsRepository,
) -> Event:
    return await event_repository.create(create_event_dto)


@pytest_asyncio.fixture
async def create_event_usecase(
    container: AsyncContainer,
) -> usecases.ReadEventUseCase:
    async with container() as nested:
        yield await nested.get(usecases.CreateEventUseCase)


@pytest_asyncio.fixture
async def read_event_usecase(
    container: AsyncContainer,
) -> usecases.CreateEventUseCase:
    async with container() as nested:
        yield await nested.get(usecases.ReadEventUseCase)


@pytest_asyncio.fixture
async def update_event_usecase(
    container: AsyncContainer,
) -> usecases.UpdateEventUseCase:
    async with container() as nested:
        yield await nested.get(usecases.UpdateEventUseCase)


@pytest_asyncio.fixture
async def delete_event_usecase(
    container: AsyncContainer,
) -> usecases.DeleteEventUseCase:
    async with container() as nested:
        yield await nested.get(usecases.DeleteEventUseCase)


@pytest_asyncio.fixture
async def deduplicate_event_usecase(
    container: AsyncContainer,
) -> usecases.DeduplicateEventUseCase:
    async with container() as nested:
        yield await nested.get(usecases.DeduplicateEventUseCase)


@pytest_asyncio.fixture
async def find_event_usecase(
    container: AsyncContainer,
) -> usecases.FindEventUseCase:
    async with container() as nested:
        yield await nested.get(usecases.FindEventUseCase)


@pytest_asyncio.fixture
async def read_all_event_usecase(
    container: AsyncContainer,
) -> usecases.ReadAllEventUseCase:
    async with container() as nested:
        yield await nested.get(usecases.ReadAllEventUseCase)


@pytest_asyncio.fixture
async def read_organization_events_usecase(
    container: AsyncContainer,
) -> usecases.ReadOrganizationEventsUseCase:
    async with container() as nested:
        yield await nested.get(usecases.ReadOrganizationEventsUseCase)


@pytest_asyncio.fixture
async def read_user_events_usecase(
    container: AsyncContainer,
) -> usecases.ReadUserEventsUseCase:
    async with container() as nested:
        yield await nested.get(usecases.ReadUserEventsUseCase)
