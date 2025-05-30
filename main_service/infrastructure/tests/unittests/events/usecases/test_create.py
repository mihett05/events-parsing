import pytest
from application.events.usecases import CreateEventUseCase
from domain.events.dtos import CreateEventDto
from domain.users.entities import User


@pytest.mark.asyncio
@pytest.mark.skip
async def test_create_success(
    create_event_usecase: CreateEventUseCase,
    create_event_dto: CreateEventDto,
    get_admin: User,
):
    create_event_dto.title = "random string"
    event = await create_event_usecase(dto=create_event_dto, actor=get_admin)

    # TODO: тут вроде проблема с часовым поясом возникает

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
