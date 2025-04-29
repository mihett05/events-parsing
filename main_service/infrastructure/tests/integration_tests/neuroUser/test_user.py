# -------------------------------------------------------
# ----------------------- USERS -------------------------
# -------------------------------------------------------
import pytest
from httpx import AsyncClient

from infrastructure.api.v1.users.models import UserModel


@pytest.mark.asyncio
async def test_get_me(async_client: AsyncClient, user_with_token_model_factory):
    user = user_with_token_model_factory()
    headers = {"Authorization": f"Bearer {user.accessToken}"}
    response = await async_client.get("/v1/users/me", headers=headers)
    assert response.status_code == 200
    result = UserModel(**response.json())
    assert result.id == user.user.id


@pytest.mark.asyncio
async def test_read_all_users(async_client: AsyncClient, user_with_token_model_factory):
    user = user_with_token_model_factory()
    headers = {"Authorization": f"Bearer {user.accessToken}"}
    response = await async_client.get("/v1/users/", headers=headers)
    assert response.status_code == 200
    result = [UserModel(**u) for u in response.json()]
    assert len(result) >= 0


@pytest.mark.asyncio
async def test_read_user_by_id(async_client: AsyncClient, user_with_token_model_factory):
    user = user_with_token_model_factory()
    headers = {"Authorization": f"Bearer {user.accessToken}"}
    response = await async_client.get(f"/v1/users/{user.user.id}", headers=headers)
    assert response.status_code == 200
    result = UserModel(**response.json())
    assert result.id == user.user.id


@pytest.mark.asyncio
async def test_update_user(async_client: AsyncClient, user_with_token_model_factory, update_user_model_dto_factory):
    user = user_with_token_model_factory()
    dto = update_user_model_dto_factory()
    headers = {"Authorization": f"Bearer {user.accessToken}"}
    response = await async_client.put(f"/v1/users/{user.user.id}", json=dto.model_dump(by_alias=True), headers=headers)
    assert response.status_code == 200
    result = UserModel(**response.json())
    assert result.fullname == dto.fullname
    assert result.telegramId == dto.telegramId
