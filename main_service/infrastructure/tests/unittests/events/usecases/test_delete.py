import random

import pytest
from application.events.usecases import DeleteEventUseCase, ReadEventUseCase
from domain.events.entities import Event
from domain.events.exceptions import EventNotFoundError
from domain.users.entities import User


@pytest.mark.asyncio
async def test_delete_success(
    read_event_usecase: ReadEventUseCase,
    delete_event_usecase: DeleteEventUseCase,
    create_event,
    get_admin: User,  # noqa
):
    event = await delete_event_usecase(create_event.id, get_admin)
    assert event == create_event

    with pytest.raises(EventNotFoundError):
        await read_event_usecase(event.id, get_admin)


@pytest.mark.asyncio
async def test_delete_not_found(
    delete_event_usecase: DeleteEventUseCase, get_admin: User
):
    with pytest.raises(EventNotFoundError):
        await delete_event_usecase(random.randint(100, 200), get_admin)
