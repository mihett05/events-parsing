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
async def create_event_dto() -> CreateEventDto:
    date = datetime.now().date()
    return CreateEventDto(
        title="Example",
        type=EventTypeEnum.HACKATHON,
        format=EventFormatEnum.OFFLINE,
        location=None,
        description="Example Description",
        organization_id=None,
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
async def read_all_events_dto() -> ReadAllEventsDto:
    return ReadAllEventsDto(
        page=0,
        page_size=50,
        start_date=datetime.combine(datetime.now().date(), datetime.min.time()),
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


@pytest_asyncio.fixture
async def create_event(
    create_event_dto: CreateEventDto,
    events_repository: EventsRepository,
) -> Callable[..., Coroutine[Any, Any, Event]]:
    async def _factory() -> Event:
        return await events_repository.create(create_event_dto)

    return _factory


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare(pytestconfig: pytest.Config, events_repository: EventsRepository):
    if pytestconfig.getoption("--integration", default=False):
        return
    await events_repository.clear()  # noqa


@pytest_asyncio.fixture(scope="function", autouse=True)
async def teardown(pytestconfig: pytest.Config, events_repository: EventsRepository):
    yield
    if pytestconfig.getoption("--integration", default=False):
        return
    await events_repository.clear()  # noqa


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare(
    pytestconfig: pytest.Config,
    users_repository: UsersRepository,
):
    if pytestconfig.getoption("--integration", default=False):
        return
    await users_repository.clear()  # noqa
