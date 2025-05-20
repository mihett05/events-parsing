import random

import pytest
from application.events.usecases import ReadEventUseCase
from domain.events.entities import Event
from domain.events.exceptions import EventNotFoundError


@pytest.mark.asyncio
async def test_read_success(
    read_event_usecase: ReadEventUseCase, create_event, create_user1
):
    create_event = await create_event()
    user = await create_user1()

    event = await read_event_usecase(create_event.id, user)
    assert event == create_event


@pytest.mark.asyncio
async def test_read_not_found(
    read_event_usecase: ReadEventUseCase, create_user1
):
    user = await create_user1()

    with pytest.raises(EventNotFoundError):
        await read_event_usecase(random.randint(100, 200), user)
