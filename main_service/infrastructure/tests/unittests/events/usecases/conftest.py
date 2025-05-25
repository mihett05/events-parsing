import application.events.usecases as usecases
import pytest_asyncio
from dishka import AsyncContainer


@pytest_asyncio.fixture
async def create_event_usecase(
    container: AsyncContainer,
) -> usecases.CreateEventUseCase:
    async with container() as nested:
        yield await nested.get(usecases.CreateEventUseCase)


@pytest_asyncio.fixture
async def read_event_usecase(
    container: AsyncContainer,
) -> usecases.ReadEventUseCase:
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
async def read_feed_events_usecase(
    container: AsyncContainer,
) -> usecases.ReadForFeedEventsUseCase:
    async with container() as nested:
        yield await nested.get(usecases.ReadForFeedEventsUseCase)
