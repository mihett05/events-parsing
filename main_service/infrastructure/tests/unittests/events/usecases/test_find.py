from datetime import timedelta

import pytest
from application.events.usecases import FindEventUseCase
from domain.events.dtos import CreateEventDto
from domain.events.entities import Event


@pytest.mark.asyncio
async def test_find_success(
    find_event_usecase: FindEventUseCase,
    create_event_dto: CreateEventDto,
    create_event,
):
    create_event = await create_event()
    event = await find_event_usecase(create_event_dto)
    assert event is not None
    print(event)
    print()
    print(create_event)
    attrs = [
        attr
        for attr in dir(Event)
        if not attr.startswith("__") and not callable(getattr(Event, attr))
    ]
    for attr in attrs:
        assert getattr(event, attr) == getattr(create_event, attr)


@pytest.mark.asyncio
async def test_find_not_found(
    find_event_usecase: FindEventUseCase,
    create_event_dto: CreateEventDto,
):
    create_event_dto.end_registration -= timedelta(days=1)
    event = await find_event_usecase(create_event_dto)
    assert event is None
