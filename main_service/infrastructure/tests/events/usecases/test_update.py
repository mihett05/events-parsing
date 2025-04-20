from copy import copy

import pytest

from application.events.dtos import UpdateEventDto
from application.events.usecases import UpdateEventUseCase
from domain.events.entities import Event
from domain.events.exceptions import EventNotFound


@pytest.mark.asyncio
async def test_update_success(
    update_event_usecase: UpdateEventUseCase,
    update_event_dto: UpdateEventDto,
    create_event: Event,
):
    create_event = copy(create_event)
    event = await update_event_usecase(update_event_dto, None)

    assert event.title != create_event.title
    assert event.description != create_event.description

    assert event.title == update_event_dto.title
    assert event.description == update_event_dto.description


@pytest.mark.asyncio
async def test_update_not_found(
    update_event_usecase: UpdateEventUseCase,
    update_event_dto: UpdateEventDto,
):
    update_event_dto.event_id = 42
    with pytest.raises(EventNotFound):
        _ = await update_event_usecase(update_event_dto, None)
