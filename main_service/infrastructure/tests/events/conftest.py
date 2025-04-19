from datetime import datetime, timedelta

import pytest_asyncio
from dishka import AsyncContainer

import application.events.usecases as usecases
from application.events.dtos import UpdateEventDto
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
    yield await container.get(EventsRepository)


@pytest_asyncio.fixture
async def create_event(
    create_event_dto: CreateEventDto,
    event_repository: EventsRepository,
) -> Event:
    return await event_repository.create(create_event_dto)
