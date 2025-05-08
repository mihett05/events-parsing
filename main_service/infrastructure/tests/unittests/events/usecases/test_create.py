import pytest
from application.events.usecases import CreateEventUseCase
from domain.events.dtos import CreateEventDto


@pytest.mark.asyncio
async def test_create_success(
    create_event_usecase: CreateEventUseCase,
    create_event_dto: CreateEventDto,
    create_user1
):
    user = await create_user1()
    event = await create_event_usecase(dto=create_event_dto, actor=user)

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

    assert event.id == 1
