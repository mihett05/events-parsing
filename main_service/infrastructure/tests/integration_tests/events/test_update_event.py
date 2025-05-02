import pytest
from httpx import AsyncClient
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from infrastructure.api.v1.events.models import EventModel


@pytest.mark.asyncio
async def test_update_event_success(
    generate_events: list[EventModel],
    async_client: AsyncClient,
    user_with_token_model,
    update_event_model_dto_factory,
):
    event_model = generate_events[0]
    dto = update_event_model_dto_factory()
    headers = {"Authorization": f"Bearer {user_with_token_model.access_token}"}


    response = await async_client.put(
        f"/v1/events/{event_model.id}",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == HTTP_200_OK

    response2 = await async_client.get(f"/v1/events/{event_model.id}")
    event_model = EventModel(**response2.json())

    assert event_model.title == dto.title
    assert event_model.description == dto.description

@pytest.mark.asyncio
async def test_update_event_unauthorized(
    generate_events: list[EventModel],
    async_client: AsyncClient,
    user_with_token_model,
    update_event_model_dto_factory,
):
    dto = update_event_model_dto_factory()
    headers = {"Authorization": f"Bearer Bismillahov Bismillah Bismillahovich"}


    response = await async_client.put(
        "/v1/events/228",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_update_event_not_found(
    generate_events: list[EventModel],
    async_client: AsyncClient,
    user_with_token_model,
    update_event_model_dto_factory,
    create_event_model_dto_factory
):
    dto = create_event_model_dto_factory()
    headers = {"Authorization": f"Bearer {user_with_token_model.access_token}"}
    response = await async_client.post(
        "/v1/events/",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    result = EventModel(**response.json())

    await async_client.delete(f"/v1/events/{result.id}", headers=headers)

    response = await async_client.put(
        f"/v1/events/{result.id}",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_event_unprocessable_entity(
    generate_events: list[EventModel],
    async_client: AsyncClient,
    user_with_token_model,
    update_event_model_dto_factory,
):
    event_model = generate_events[0]
    dto = update_event_model_dto_factory()
    dto.title = None
    headers = {"Authorization": f"Bearer {user_with_token_model.access_token}"}


    response = await async_client.put(
        f"/v1/events/{event_model.id}",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
