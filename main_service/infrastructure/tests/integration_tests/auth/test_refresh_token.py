from typing import Callable, Coroutine, Any

import pytest
from httpx import AsyncClient
from starlette import status

from infrastructure.api.v1.auth.dtos import AuthenticateUserModelDto
from infrastructure.api.v1.auth.models import UserWithTokenModel


@pytest.mark.asyncio
async def test_refresh_token_success(
    async_client: AsyncClient,
    authenticate_dto_factory: Callable[[], AuthenticateUserModelDto],
    user_with_token_model: Callable[..., Coroutine[Any, Any, UserWithTokenModel]],
):
    user_with_token = await user_with_token_model()
    response = await async_client.post(
        "/v1/auth/login",
        json=authenticate_dto_factory().model_dump(by_alias=True, mode="json"),
    )
    async_client.cookies.set("refresh", response.cookies.get("refresh"))
    response2 = await async_client.post("/v1/auth/refresh")

    print(response.json())
    assert response2.status_code == status.HTTP_200_OK


    response_model = UserWithTokenModel(**response2.json())
    attrs = (
        "email",
        "fullname",
        "is_active",
        "telegram_id",
    )

    for attr in attrs:
        assert getattr(user_with_token.user, attr) == getattr(response_model.user, attr)


@pytest.mark.asyncio
async def test_refresh_token_invalid(
    async_client: AsyncClient,
    authenticate_dto_factory: Callable[[], AuthenticateUserModelDto],
    user_with_token_model: Callable[..., Coroutine[Any, Any, UserWithTokenModel]],
):
    async_client.cookies.set("refresh", "bismillah allah")
    response = await async_client.post("/v1/auth/refresh")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
