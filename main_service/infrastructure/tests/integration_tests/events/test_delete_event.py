from typing import Any, Callable, Coroutine

import pytest
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)

from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.events.models import EventModel


@pytest.mark.asyncio
async def test_delete_event_success(
    async_client: AsyncClient,
    user_with_token_model: Callable[..., Coroutine[Any, Any, UserWithTokenModel]],
    create_event_model_dto_factory,
):
    dto = create_event_model_dto_factory()
    user_with_token = await user_with_token_model()
    headers = {"Authorization": f"Bearer {user_with_token.access_token}"}
    response = await async_client.post(
        "/v1/events/",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    result = EventModel(**response.json())

    response = await async_client.delete(f"/v1/events/{result.id}", headers=headers)
    assert response.status_code == HTTP_200_OK

    result = EventModel(**response.json())
    response = await async_client.get(f"/v1/events/{result.id}", headers=headers)
    assert response.status_code == HTTP_404_NOT_FOUND
    assert result.title == dto.title


@pytest.mark.asyncio
async def test_delete_event_not_found(
    async_client: AsyncClient,
    user_with_token_model: Callable[..., Coroutine[Any, Any, UserWithTokenModel]],
    create_event_model_dto_factory,
):
    dto = create_event_model_dto_factory()
    user_with_token = await user_with_token_model()
    headers = {"Authorization": f"Bearer {user_with_token.access_token}"}
    response = await async_client.post(
        "/v1/events/",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    result = EventModel(**response.json())

    await async_client.delete(f"/v1/events/{result.id}", headers=headers)
    response = await async_client.delete(f"/v1/events/{result.id}", headers=headers)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_event_unauthorized(
    async_client: AsyncClient,
):
    headers = {"Authorization": f"Bearer Bismillahov Bismillah Bismillahovich"}

    response = await async_client.delete("/v1/events/69", headers=headers)
    assert response.status_code == HTTP_401_UNAUTHORIZED
