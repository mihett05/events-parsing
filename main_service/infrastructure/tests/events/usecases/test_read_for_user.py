import pytest
from application.events.usecases import ReadUserEventsUseCase
from domain.events.dtos import ReadUserEventsDto


@pytest.mark.asyncio
async def test_read_organization_events_success(
    read_user_events_usecase: ReadUserEventsUseCase,
    read_user_events_dto: ReadUserEventsDto,
):
    with pytest.raises(NotImplementedError):
        await read_user_events_usecase(read_user_events_dto)
