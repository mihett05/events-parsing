import pytest
from application.events.usecases import DeduplicateEventUseCase
from domain.events.dtos import CreateEventDto
from domain.events.entities import Event


@pytest.mark.asyncio
async def test_deduplicate_create_new(
    deduplicate_event_usecase: DeduplicateEventUseCase,
    create_event_dto: CreateEventDto,
):
    event, _ = await deduplicate_event_usecase(None, create_event_dto)

    attrs = (
        "title",
        "type",
        "format",
        "location",
        "description",
        "end_date",
        "start_date",
        "end_registration",
    )
    for attr in attrs:
        assert getattr(event, attr) == getattr(create_event_dto, attr)


@pytest.mark.asyncio
async def test_deduplicate_found_one(
    deduplicate_event_usecase: DeduplicateEventUseCase,
    create_event_dto: CreateEventDto,
    create_event: Event,
):
    event, _ = await deduplicate_event_usecase(None, create_event_dto)
    assert event == create_event
