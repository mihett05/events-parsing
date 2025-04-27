import pytest

from application.events.usecases import ReadForFeedEventsUseCase
from domain.events.dtos import ReadAllEventsFeedDto
from domain.events.entities import Event


@pytest.mark.asyncio
async def test_read_all_success(
        read_feed_events_usecase: ReadForFeedEventsUseCase,
        read_feed_events_dto: ReadAllEventsFeedDto,
        create_event: Event,
):
    events = await read_feed_events_usecase(read_feed_events_dto)

    assert len(events) == 1
    assert events[0] == create_event


@pytest.mark.asyncio
async def test_read_all_empty(
        read_feed_events_usecase: ReadForFeedEventsUseCase,
        read_feed_events_dto: ReadAllEventsFeedDto,
):
    read_feed_events_dto.page = 10
    events = await read_feed_events_usecase(read_feed_events_dto)

    assert len(events) == 0
