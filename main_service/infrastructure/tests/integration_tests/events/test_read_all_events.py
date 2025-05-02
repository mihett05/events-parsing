import random
from datetime import datetime

import pytest
import pytz
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
    response = await async_client.get(
        f"/v1/events/feed", params={"page": page, "page_size": page_size}
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_read_events_success_dating(
    generate_events: list[EventModel],
    async_client: AsyncClient,
    create_event_model_dto_factory,
):
    start_date = datetime(2025, 3, 2).replace(tzinfo=pytz.utc)
    end_date = datetime(2025, 12, 2).replace(tzinfo=pytz.utc)
    response = await async_client.get(
        f"/v1/events/feed",
        params={
            "page": 0,
            "page_size": 50,
            "start_date": start_date,
            "end_date": end_date,
        },
    )
    assert response.status_code == status.HTTP_200_OK

    models = response.json()
    for model in models:
        model_start_date = datetime.fromisoformat(model["startDate"])
        model_end_date = datetime.fromisoformat(model["endDate"])

        period_contains_start = start_date <= model_start_date <= end_date
        period_contains_end = start_date <= model_end_date <= end_date

        assert period_contains_start or period_contains_end


@pytest.mark.asyncio
async def test_read_events_success_organization(
    generate_events: list[EventModel],
    async_client: AsyncClient,
    create_event_model_dto_factory,
):
    response = await async_client.get("/v1/organizations/")
    org = random.choice(response.json())

    response = await async_client.get(f"/v1/events/feed", params={"organization_id": org["id"]})
    assert response.status_code == status.HTTP_200_OK
    models = response.json()
    for model in models:
        assert model["organizationId"] == org["id"]


@pytest.mark.asyncio
async def test_read_events_bad_request(
    generate_events: list[EventModel],
    async_client: AsyncClient,
    create_event_model_dto_factory,
):
    start_date = datetime(2025, 3, 2).replace(tzinfo=pytz.utc)
    end_date = datetime(2025, 12, 2).replace(tzinfo=pytz.utc)
    response = await async_client.get(
        f"/v1/events/feed",
        params={
            "page": 0,
            "page_size": 50,
            "start_date": end_date,
            "end_date": start_date,
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
