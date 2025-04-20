import pytest

from application.events.usecases import ReadAllEventUseCase
from domain.events.dtos import ReadAllEventsDto
from domain.events.entities import Event


@pytest.mark.asyncio
async def test_read_all_success(
    read_all_event_usecase: ReadAllEventUseCase,
    read_all_events_dto: ReadAllEventsDto,
    create_event: Event,
):
    events = await read_all_event_usecase(read_all_events_dto)

    assert len(events) == 1
    assert events[0] == create_event


@pytest.mark.asyncio
async def test_read_all_empty(
    read_all_event_usecase: ReadAllEventUseCase,
    read_all_events_dto: ReadAllEventsDto,
):
    read_all_events_dto.page = 10
    events = await read_all_event_usecase(read_all_events_dto)

    assert len(events) == 0
