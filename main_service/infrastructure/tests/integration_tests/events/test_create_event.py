import pytest
from httpx import AsyncClient

from infrastructure.api.v1.events.models import EventModel


@pytest.mark.asyncio
async def test_create_event(
    async_client: AsyncClient,
    user_with_token_model,
    create_event_model_dto_factory,
):
    dto = create_event_model_dto_factory()
    headers = {"Authorization": f"Bearer {user_with_token_model.access_token}"}
    response = await async_client.post(
        "/v1/events/",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == 200
    result = EventModel(**response.json())
    assert result.title == dto.title
    assert result.type == dto.type
    assert result.organization_id == dto.organization_id