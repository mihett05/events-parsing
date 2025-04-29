# -------------------------------------------------------
# ----------------------- AUTH --------------------------
# -------------------------------------------------------
import pytest
from httpx import AsyncClient

from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.users.models import UserModel


@pytest.mark.asyncio
async def test_register_user(
    async_client: AsyncClient, create_user_model_dto_factory
):
    payload = create_user_model_dto_factory()
    response = await async_client.post(
        "/v1/auth/register", json=payload.model_dump(by_alias=True)
    )
    assert response.status_code == 200
    result = UserWithTokenModel(**response.json())
    assert isinstance(result.user, UserModel)
    assert result.access_token is not None


@pytest.mark.asyncio
async def test_login_user(
    async_client: AsyncClient, authenticate_user_model_dto_factory
):
    # Р РµРіРёСЃС‚СЂРёСЂСѓРµРј РїРµСЂРµРґ Р»РѕРіРёРЅРѕРј
    payload = authenticate_user_model_dto_factory()
    await async_client.post(
        "/v1/auth/register", json=payload.model_dump(by_alias=True)
    )

    response = await async_client.post(
        "/v1/auth/login", json=payload.model_dump(by_alias=True)
    )
    assert response.status_code == 200
    result = UserWithTokenModel(**response.json())
    assert isinstance(result.user, UserModel)


@pytest.mark.asyncio
async def test_refresh_token(
    async_client: AsyncClient, user_with_token_model_factory
):
    user = user_with_token_model_factory()
    response = await async_client.post(
        "/v1/auth/refresh", cookies={"refresh": "fake-refresh-token"}
    )
    assert response.status_code == 200
    result = UserWithTokenModel(**response.json())
    assert result.access_token != user.access_token
