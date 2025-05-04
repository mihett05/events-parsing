import pytest
from httpx import AsyncClient

from infrastructure.api.v1.users.models import UserModel


@pytest.mark.asyncio
async def test_read_user_by_id(async_client: AsyncClient, user_with_token_model):
    user = user_with_token_model
    headers = {"Authorization": f"Bearer {user.access_token}"}
    response = await async_client.get(f"/v1/users/{user.user.id}", headers=headers)
    assert response.status_code == 200
    result = UserModel(**response.json())
    assert result.id == user.user.id
