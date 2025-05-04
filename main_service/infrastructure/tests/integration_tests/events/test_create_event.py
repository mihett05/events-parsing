from datetime import datetime
from typing import Any, Callable, Coroutine

import pytest
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.events.models import EventModel


@pytest.mark.asyncio
async def test_create_event_success(
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
    assert response.status_code == HTTP_200_OK
    result = EventModel(**response.json())
    assert result.title == dto.title
    assert result.type == dto.type
    assert result.organization_id == dto.organization_id
    await async_client.delete(f"/v1/events/{result.id}", headers=headers)


@pytest.mark.asyncio
async def test_create_event_unprocessed_entity(
    async_client: AsyncClient,
    user_with_token_model: Callable[..., Coroutine[Any, Any, UserWithTokenModel]],
    create_event_model_dto_factory,
):
    dto = create_event_model_dto_factory()
    user_with_token = await user_with_token_model()
    dto.title = None
    headers = {"Authorization": f"Bearer {user_with_token.access_token}"}
    response = await async_client.post(
        "/v1/events/",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_event_unauthorized(
    async_client: AsyncClient,
    create_event_model_dto_factory,
):
    dto = create_event_model_dto_factory()
    headers = {"Authorization": f"Bearer kill nigger"}
    response = await async_client.post(
        "/v1/events/",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_create_event_period_invalid(
    async_client: AsyncClient,
    user_with_token_model: Callable[..., Coroutine[Any, Any, UserWithTokenModel]],
    create_event_model_dto_factory,
):
    dto = create_event_model_dto_factory()
    user_with_token = await user_with_token_model()
    model_json = dto.model_dump(by_alias=True, mode="json")
    model_json["startDate"], model_json["endDate"] = (
        model_json["endDate"],
        model_json["startDate"],
    )

    headers = {"Authorization": f"Bearer {user_with_token.access_token}"}
    response = await async_client.post(
        "/v1/events/",
        json=model_json,
        headers=headers,
    )

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
