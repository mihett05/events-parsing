import pytest
from httpx import AsyncClient

from infrastructure.api.v1.events.models import EventModel


@pytest.mark.asyncio
async def test_update_event(
    async_client: AsyncClient,
    user_with_token_model,
    update_event_model_dto_factory,
):
    dto = update_event_model_dto_factory()
    headers = {"Authorization": f"Bearer {user_with_token_model.access_token}"}
    response = await async_client.put(
        "/v1/events/1",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    if response.status_code == 200:
        result = EventModel(**response.json())
        assert result.title == dto.title
        assert result.description == dto.description
    else:
        assert response.status_code == 404