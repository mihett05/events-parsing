import random

import pytest
from application.events.usecases import DeleteEventUseCase, ReadEventUseCase
from domain.events.entities import Event
from domain.events.exceptions import EventNotFoundError


@pytest.mark.asyncio
async def test_delete_success(
    read_event_usecase: ReadEventUseCase,
    delete_event_usecase: DeleteEventUseCase,
    create_event,
    create_user1,
):
    create_event = await create_event()
    user = await create_user1()
    event = await delete_event_usecase(create_event.id, user)
    assert event == create_event

    with pytest.raises(EventNotFoundError):
        await read_event_usecase(event.id, user)


@pytest.mark.asyncio
async def test_delete_not_found(
    delete_event_usecase: DeleteEventUseCase, create_user1
):
    user = await create_user1()
    with pytest.raises(EventNotFoundError):
        await delete_event_usecase(random.randint(100, 200), user)
