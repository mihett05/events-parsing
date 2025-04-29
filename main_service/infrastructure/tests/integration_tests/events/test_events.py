# -------------------------------------------------------
# ---------------------- EVENTS -------------------------
# -------------------------------------------------------
import pytest
from httpx import AsyncClient

from infrastructure.api.v1.events.models import EventModel


@pytest.mark.asyncio
async def test_create_event(
    async_client: AsyncClient,
    user_with_token_model_factory,
    create_event_model_dto_factory,
):
    dto = create_event_model_dto_factory()
    headers = {
        "Authorization": f"Bearer {user_with_token_model_factory.access_token}"
    }
    response = await async_client.post(
        "/v1/events/",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == 200
    result = EventModel(**response.json())
    assert result.title == dto.title
    assert result.type == dto.type
    assert (
        result.organization_id == dto.organizationId
    )


@pytest.mark.asyncio
async def test_read_event(
    async_client: AsyncClient, user_with_token_model_factory
):
    headers = {
        "Authorization": f"Bearer {user_with_token_model_factory.access_token}"
    }
    response = await async_client.get("/v1/events/1", headers=headers)
    if response.status_code == 200:
        result = EventModel(**response.json())
        assert isinstance(result.id, int)
    else:
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_event(
    async_client: AsyncClient,
    user_with_token_model_factory,
    update_event_model_dto_factory,
):
    dto = update_event_model_dto_factory()
    headers = {
        "Authorization": f"Bearer {user_with_token_model_factory.access_token}"
    }
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
