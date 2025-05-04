import pytest
from httpx import AsyncClient
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from infrastructure.api.v1.users.models import UserModel


@pytest.mark.asyncio
async def test_get_me_success(async_client: AsyncClient, create_user):
    user_with_token = create_user
    headers = {"Authorization": f"Bearer {user_with_token.access_token}"}
    response = await async_client.get("/v1/users/me", headers=headers)
    assert response.status_code == HTTP_200_OK
    result = UserModel(**response.json())
    assert result == user_with_token.user


@pytest.mark.asyncio
async def test_get_me_unauthorized(
    async_client: AsyncClient,
):
    headers = {"Authorization": "Bearer Bismillahov Bismillah Bismillahovich"}
    response = await async_client.get("/v1/users/me", headers=headers)
    assert response.status_code == HTTP_401_UNAUTHORIZED
