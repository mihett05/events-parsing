from datetime import datetime, timedelta
from typing import Any, Callable, Coroutine

import pytest
import pytest_asyncio
from application.events.dtos import UpdateEventDto
from dishka import AsyncContainer
from domain.events.dtos import (
    CreateEventDto,
    ReadAllEventsDto,
    ReadAllEventsFeedDto,
    ReadUserEventsDto,
)
from domain.events.entities import Event
from domain.events.enums import EventFormatEnum, EventTypeEnum
from domain.events.repositories import EventsRepository
from domain.users.entities import User
from domain.users.repositories import UsersRepository


@pytest_asyncio.fixture
async def update_event_dto() -> UpdateEventDto:
    return UpdateEventDto(
        event_id=1, title="Example New", description="Example Description New"
    )


@pytest_asyncio.fixture
async def read_all_events_dto() -> ReadAllEventsDto:
    return ReadAllEventsDto(
        page=0,
        page_size=50,
        start_date=datetime.now().date(),
        for_update=False,
    )


@pytest_asyncio.fixture
async def read_feed_events_dto() -> ReadAllEventsFeedDto:
    return ReadAllEventsFeedDto(
        page=0,
        page_size=50,
        start_date=None,
        end_date=None,
        organization_id=None,
        type=None,
        format=None,
    )


@pytest_asyncio.fixture
async def read_user_events_dto() -> ReadUserEventsDto:
    return ReadUserEventsDto(
        user_id=1,
        page=0,
        page_size=50,
    )


@pytest_asyncio.fixture
async def events_repository(container: AsyncContainer) -> EventsRepository:
    async with container() as nested:
        yield await nested.get(EventsRepository)


@pytest_asyncio.fixture
async def users_repository(container: AsyncContainer) -> UsersRepository:
    async with container() as nested:
        yield await nested.get(UsersRepository)
