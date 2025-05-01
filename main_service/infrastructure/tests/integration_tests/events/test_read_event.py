import pytest
from httpx import AsyncClient
from starlette import status

from infrastructure.api.v1.events.models import EventModel


@pytest.mark.asyncio
async def test_read_event_success(
    generate_events: list[EventModel],
    async_client: AsyncClient,
    create_event_model_dto_factory,
):
    for model in generate_events:
        response = await async_client.get(f"/v1/events/{model.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == model.model_dump(by_alias=True, mode="json")

@pytest.mark.asyncio
async def test_read_event_not_found(
    generate_events: list[EventModel],
    async_client: AsyncClient,
    create_event_model_dto_factory,
):
    model = generate_events[-1]
    response = await async_client.get(f"/v1/events/{model.id + 1}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
