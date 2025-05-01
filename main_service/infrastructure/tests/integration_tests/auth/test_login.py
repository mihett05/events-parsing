from typing import Callable

import pytest
from httpx import AsyncClient
from starlette import status

from infrastructure.api.v1.auth.dtos import AuthenticateUserModelDto
from infrastructure.api.v1.auth.models import UserWithTokenModel


@pytest.mark.asyncio
async def test_login_success(
    async_client: AsyncClient,
    authenticate_dto_factory,
    user_with_token_model: UserWithTokenModel,
):
    dto = authenticate_dto_factory()
    response = await async_client.post(
        "/v1/auth/login",
        json=dto.model_dump(by_alias=True, mode="json"),
    )
    assert response.status_code == status.HTTP_200_OK

    response_model = UserWithTokenModel(**response.json())
    attrs = (
        "email",
        "fullname",
        "is_active",
        "telegram_id",
    )
    for attr in attrs:
        assert getattr(user_with_token_model.user, attr) == getattr(response_model.user, attr)


@pytest.mark.asyncio
async def test_login_unauthorized(async_client: AsyncClient, authenticate_dto_factory):
    dto = authenticate_dto_factory()
    dto.email = "broken_email@test.com"
    response = await async_client.post(
        "/v1/auth/login",
        json=dto.model_dump(by_alias=True, mode="json"),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_login_unprocessable_entity(async_client: AsyncClient, authenticate_dto_factory):
    json_with_broken_mail = {"email": "имэил", "password": "пасворд"}
    response = await async_client.post(
        "/v1/auth/login",
        json=json_with_broken_mail,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
