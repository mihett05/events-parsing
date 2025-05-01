from datetime import datetime

import pytest
from httpx import AsyncClient
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, \
    HTTP_400_BAD_REQUEST

from infrastructure.api.v1.events.models import EventModel


@pytest.mark.asyncio
async def test_create_event_success(
    async_client: AsyncClient,
    user_with_token_model,
    create_event_model_dto_factory,
):
    dto = create_event_model_dto_factory()
    headers = {"Authorization": f"Bearer {user_with_token_model.access_token}"}
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

@pytest.mark.asyncio
async def test_create_event_unprocessed_entity(
    async_client: AsyncClient,
    user_with_token_model,
    create_event_model_dto_factory,
):
    dto = create_event_model_dto_factory()
    dto.title = None
    headers = {"Authorization": f"Bearer {user_with_token_model.access_token}"}
    response = await async_client.post(
        "/v1/events/",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.asyncio
async def test_create_event_forbidden(
    async_client: AsyncClient,
    create_event_model_dto_factory,
):
    dto = create_event_model_dto_factory()
    response = await async_client.post(
        "/v1/events/",
        json=dto.model_dump(by_alias=True, mode="json"),
    )
    assert response.status_code == HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_create_event_period_invalid(
    async_client: AsyncClient,
    user_with_token_model,
    create_event_model_dto_factory,
):
    dto = create_event_model_dto_factory()
    model_json = dto.model_dump(by_alias=True, mode="json")
    model_json["startDate"], model_json["endDate"] = model_json["endDate"], model_json["startDate"]

    headers = {"Authorization": f"Bearer {user_with_token_model.access_token}"}
    response = await async_client.post(
        "/v1/events/",
        json=model_json,
        headers=headers,
    )

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY