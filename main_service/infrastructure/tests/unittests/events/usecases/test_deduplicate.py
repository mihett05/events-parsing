import pytest
from application.events.usecases import DeduplicateEventUseCase, ReadEventUseCase
from application.transactions import TransactionsGateway
from domain.events.dtos import CreateEventDto
from domain.events.entities import Event
from domain.users.entities import User


@pytest.mark.asyncio
async def test_deduplicate_create_new(
    deduplicate_event_usecase: DeduplicateEventUseCase,
    read_event_usecase: ReadEventUseCase,
    create_event_dto: CreateEventDto,
    get_admin: User,  # noqa
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
    get_admin: User,  # noqa
    get_admin_event: Event,
):
    event, _ = await deduplicate_event_usecase(None, create_event_dto)
    assert event == get_admin_event
