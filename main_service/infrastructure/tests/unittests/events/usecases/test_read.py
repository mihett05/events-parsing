import random

import pytest
from application.events.usecases import ReadEventUseCase
from domain.events.entities import Event
from domain.events.exceptions import EventNotFoundError


@pytest.mark.asyncio
async def test_read_success(
    read_event_usecase: ReadEventUseCase,
    create_event
):
    create_event = await create_event()
    # TODO: добавить актора
    event = await read_event_usecase(create_event.id)
    assert event == create_event


@pytest.mark.asyncio
async def test_read_not_found(read_event_usecase: ReadEventUseCase):
    # TODO: добавить актора
    with pytest.raises(EventNotFoundError):
        await read_event_usecase(random.randint(100, 200))
