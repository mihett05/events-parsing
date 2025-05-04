from typing import Any, Callable, Coroutine

import pytest
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
)

from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.users.models import UserModel


@pytest.mark.asyncio
async def test_read_user_by_id(
    async_client: AsyncClient,
    user_with_token_model: Callable[..., Coroutine[Any, Any, UserWithTokenModel]],
):
    user_with_token = await user_with_token_model()
    response = await async_client.get(f"/v1/users/{user_with_token.user.id}")
    assert response.status_code == HTTP_200_OK
    result = UserModel(**response.json())
    assert result == user_with_token.user


@pytest.mark.asyncio
async def test_read_user_by_id_not_found(async_client: AsyncClient, create_user_model_dto_factory):
    dto = create_user_model_dto_factory()
    response = await async_client.post(
        "/v1/auth/register", json=dto.model_dump(by_alias=True, mode="json")
    )
    user_with_token = UserWithTokenModel(**response.json())
    headers = {"Authorization": f"Bearer {user_with_token.access_token}"}
    await async_client.delete("/v1/users/", headers=headers)

    response = await async_client.get(f"/v1/users/{user_with_token.user.id}")
    assert response.status_code == HTTP_404_NOT_FOUND
