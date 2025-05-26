import random

import pytest
from application.events.usecases import ReadEventUseCase
from domain.events.entities import Event
from domain.events.exceptions import EventNotFoundError
from domain.users.entities import User


@pytest.mark.asyncio
async def test_read_success(
    read_event_usecase: ReadEventUseCase, get_admin_event: Event, get_admin: User
):
    event = await read_event_usecase(get_admin_event.id, get_admin)
    assert event == get_admin_event


@pytest.mark.asyncio
async def test_read_not_found(read_event_usecase: ReadEventUseCase, get_admin: User):
    with pytest.raises(EventNotFoundError):
        await read_event_usecase(random.randint(100, 200), get_admin)
