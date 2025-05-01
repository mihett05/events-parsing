import pytest
from httpx import AsyncClient
from starlette import status

from infrastructure.api.v1.events.models import EventModel


@pytest.mark.asyncio
async def test_read_event_success(async_client: AsyncClient, user_with_token_model):
    headers = {"Authorization": f"Bearer {user_with_token_model.access_token}"}
    response = await async_client.get("/v1/events/1", headers=headers)
    if response.status_code == status.HTTP_200_OK:
        result = EventModel(**response.json())
        assert isinstance(result.id, int)
    else:
        assert response.status_code == status.HTTP_404_NOT_FOUND