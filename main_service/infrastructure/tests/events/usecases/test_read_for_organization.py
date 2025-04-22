import pytest
from application.events.usecases import ReadOrganizationEventsUseCase
from domain.events.dtos import ReadOrganizationEventsDto


@pytest.mark.asyncio
async def test_read_organization_events_success(
    read_organization_events_usecase: ReadOrganizationEventsUseCase,
    read_organization_events_dto: ReadOrganizationEventsDto,
):
    with pytest.raises(NotImplementedError):
        await read_organization_events_usecase(read_organization_events_dto)
