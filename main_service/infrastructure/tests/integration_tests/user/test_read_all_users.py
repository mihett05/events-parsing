import pytest
from httpx import AsyncClient

from infrastructure.api.v1.users.models import UserModel


@pytest.mark.asyncio
async def test_read_all_users(async_client: AsyncClient, user_with_token_model):
    user = user_with_token_model
    headers = {"Authorization": f"Bearer {user.access_token}"}
    response = await async_client.get("/v1/users/", headers=headers)
    assert response.status_code == 200
    result = [UserModel(**u) for u in response.json()]
    assert len(result) >= 0
