from copy import copy

import pytest
from application.events.dtos import UpdateEventDto
from application.events.usecases import UpdateEventUseCase
from domain.events.entities import Event
from domain.events.exceptions import EventNotFoundError


@pytest.mark.asyncio
async def test_update_success(
    update_event_usecase: UpdateEventUseCase,
    update_event_dto: UpdateEventDto,
    create_event,
    create_user1,
):
    create_event = await create_event()
    user = await create_user1()

    create_event = copy(create_event)
    event = await update_event_usecase(update_event_dto, user)

    assert event.title != create_event.title
    assert event.description != create_event.description

    assert event.title == update_event_dto.title
    assert event.description == update_event_dto.description


@pytest.mark.asyncio
async def test_update_not_found(
    update_event_usecase: UpdateEventUseCase,
    update_event_dto: UpdateEventDto,
    create_user1,
):
    update_event_dto.event_id = 42
    user = await create_user1()

    with pytest.raises(EventNotFoundError):
        _ = await update_event_usecase(update_event_dto, user)
