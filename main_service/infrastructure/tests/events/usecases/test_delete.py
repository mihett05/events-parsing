import random

import pytest
from application.events.usecases import DeleteEventUseCase, ReadEventUseCase
from domain.events.entities import Event
from domain.events.exceptions import EventNotFound


@pytest.mark.asyncio
async def test_delete_success(
    read_event_usecase: ReadEventUseCase,
    delete_event_usecase: DeleteEventUseCase,
    create_event: Event,
):
    event = await delete_event_usecase(create_event.id, None)
    assert event == create_event

    with pytest.raises(EventNotFound):
        await read_event_usecase(event.id)


@pytest.mark.asyncio
async def test_delete_not_found(
    delete_event_usecase: DeleteEventUseCase,
):
    with pytest.raises(EventNotFound):
        await delete_event_usecase(random.randint(100, 200), None)
