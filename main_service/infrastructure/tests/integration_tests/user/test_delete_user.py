from typing import Callable

import pytest
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
)

from infrastructure.api.v1.auth.dtos import CreateUserModelDto
from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.users.models import UserModel


@pytest.mark.asyncio
async def test_delete_user_success(
    create_user_model_dto_factory: Callable[..., CreateUserModelDto],
    async_client: AsyncClient,
):
    response = await async_client.post(
        "/v1/auth/register",
        json=create_user_model_dto_factory().model_dump(by_alias=True, mode="json"),
    )
    model = UserWithTokenModel(**response.json())
    headers = {"Authorization": f"Bearer {model.access_token}"}
    user = model.user

    response = await async_client.delete("/v1/users/", headers=headers)

    assert response.status_code == HTTP_200_OK
    assert user == UserModel(**response.json())


@pytest.mark.asyncio
async def test_delete_user_unauthorized(
    create_user_model_dto_factory: Callable[..., CreateUserModelDto],
    async_client: AsyncClient,
):
    headers = {"Authorization": "Bearer Bismillahov Bismillah Bismillahovich"}

    response = await async_client.delete("/v1/users/", headers=headers)

    assert response.status_code == HTTP_401_UNAUTHORIZED
