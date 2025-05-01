from datetime import datetime

import pytest
from httpx import AsyncClient
from starlette import status

from infrastructure.api.v1.events.models import EventModel


@pytest.mark.asyncio
async def test_read_events_success_paging(
    generate_events: list[EventModel],
    async_client: AsyncClient,
    create_event_model_dto_factory,
):
    page = 9
    page_size = 11
    response = await async_client.get(f"/v1/events/feed", params={"page": page, "page_size": page_size})
    assert response.status_code == status.HTTP_200_OK

    models = response.json()
    assert len(models) == min((page + 1) * page_size, len(generate_events)) - min(page * page_size, len(generate_events))
    for i in range(len(models)):
        assert models[i] == generate_events[page * page_size + i].model_dump(by_alias=True, mode="json")


@pytest.mark.asyncio
async def test_read_events_success_dating(
    generate_events: list[EventModel],
    async_client: AsyncClient,
    create_event_model_dto_factory,
):
    start_date = datetime(2025, 3,2)
    end_date = datetime(2025, 5,2)
    response = await async_client.get(
        f"/v1/events/feed",
        params={"page": 0, "page_size": 50, "start_date": start_date, "end_date": end_date}
    )
    print(response.json())
    assert response.status_code == status.HTTP_200_OK


    models = response.json()
    for model in models:
        assert datetime(model["start_date"]) >= start_date
        assert datetime(model["end_date"]) <= start_date

@pytest.mark.asyncio
async def test_read_events_success_organization(
    generate_events: list[EventModel],
    async_client: AsyncClient,
    create_event_model_dto_factory,
):
    response = await async_client.get(
        f"/v1/events/feed",
        params={"organization_id": 3}
    )
    assert response.status_code == status.HTTP_200_OK