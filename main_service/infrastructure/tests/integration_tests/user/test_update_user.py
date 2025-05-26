import pytest
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.users.models import UserModel


@pytest.mark.asyncio
async def test_update_user_success(
    create_users: list[UserWithTokenModel],
    async_client: AsyncClient,
    update_user_model_dto_factory,
):
    user_with_token = create_users[0]
    dto = update_user_model_dto_factory()
    headers = {"Authorization": f"Bearer {user_with_token.access_token}"}

    response = await async_client.put(
        "/v1/users/me",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == HTTP_200_OK

    response2 = await async_client.get(f"/v1/users/{user_with_token.user.id}")
    user_model = UserModel(**response2.json())

    assert user_model.fullname == dto.fullname


@pytest.mark.asyncio
async def test_update_user_unauthorized(async_client: AsyncClient, update_user_model_dto_factory):
    dto = update_user_model_dto_factory()
    headers = {"Authorization": "Bearer Bismillahov Bismillah Bismillahovich"}

    response = await async_client.put(
        "/v1/users/me",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_update_phantom_user_unauthorized(
    create_users: list[UserWithTokenModel],
    async_client: AsyncClient,
    update_user_model_dto_factory,
    create_user_model_dto_factory,
):
    master_user_with_token = create_users[0]
    dto_create = create_user_model_dto_factory()
    headers = {"Authorization": f"Bearer {master_user_with_token.access_token}"}
    response = await async_client.post(
        "/v1/auth/register",
        json=dto_create.model_dump(by_alias=True, mode="json"),
    )

    await async_client.delete("/v1/users/", headers=headers)

    dto_update = update_user_model_dto_factory()
    response2 = await async_client.put(
        "/v1/users/me",
        json=dto_update.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response2.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_update_user_unprocessable_entity(
    create_users: list[UserWithTokenModel],
    async_client: AsyncClient,
    update_user_model_dto_factory,
):
    user_with_token = create_users[0]
    dto = update_user_model_dto_factory()
    dto.fullname = None
    headers = {"Authorization": f"Bearer {user_with_token.access_token}"}

    response = await async_client.put(
        "/v1/users/me",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
