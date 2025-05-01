import random
from datetime import datetime, timedelta
from typing import Callable, Optional

import pytest
import pytest_asyncio

from domain.events.enums import EventTypeEnum, EventFormatEnum
from infrastructure.api.v1.events.dtos import (
    CreateEventModelDto,
    UpdateEventModelDto,
)
from infrastructure.api.v1.events.models import EventModel
from infrastructure.tests.integration_tests.conftest import random_string_factory, async_client


@pytest.fixture
def event_model_factory() -> Callable[[], EventModel]:
    def _factory(
        id: int = 100,
        title: str = "Test Event",
        type_: str = "conference",
        format_: str = "online",
        created_at: datetime = datetime.now(),
        is_visible: bool = True,
        location: Optional[str] = None,
        description: Optional[str] = "This is a test event",
        start_date: datetime = datetime.now(),
        end_date: Optional[datetime] = None,
        end_registration: Optional[datetime] = None,
        organization_id: Optional[int] = None,
    ) -> EventModel:
        return EventModel(
            id=id,
            title=title,
            type_=type_,
            format_=format_,
            created_at=created_at,
            is_visible=is_visible,
            location=location,
            description=description,
            start_date=start_date,
            end_date=end_date,
            end_registration=end_registration,
            organization_id=organization_id,
        )

    return _factory


@pytest.fixture
def create_event_model_dto_factory() -> Callable[[], CreateEventModelDto]:
    def _factory(
        title: str = "New Event",
        type_: EventTypeEnum = EventTypeEnum.OTHER,
        format_:  EventFormatEnum = EventFormatEnum.OTHER,
        location: Optional[str] = "Moscow",
        description: Optional[str] = "Some workshop",
        end_date: datetime = datetime(2025, 12, 31),
        start_date: datetime = datetime(2025, 12, 1),
        end_registration: datetime = datetime(2025, 11, 30),
        organization_id: int | None = None,
    ) -> CreateEventModelDto:
        return CreateEventModelDto(
            title=title,
            type=type_,
            format=format_,
            location=location,
            description=description,
            endDate=end_date,
            startDate=start_date,
            endRegistration=end_registration,
            organization_id=organization_id,
        )

    return _factory


@pytest.fixture
def update_event_model_dto_factory() -> Callable[[], UpdateEventModelDto]:
    def _factory(
        title: str = "Updated Title", description: str = "Updated Description"
    ) -> UpdateEventModelDto:
        return UpdateEventModelDto(title=title, description=description)

    return _factory

@pytest.fixture
def create_event_model_dtos(
    create_event_model_dto_factory: Callable[..., CreateEventModelDto],
    random_string_factory
) -> list[CreateEventModelDto]:
    dtos = []
    for i in range(100):
        date = datetime(2020, 1, 1)
        start_date = date + timedelta(days=random.randint(0, 2000))
        dtos.append(create_event_model_dto_factory(
            title=f"{random_string_factory(10)}",
            organization_id=random.randint(60, 70),
            start_date=start_date,
            end_date=start_date + timedelta(days=random.randint(0, 7))
        ))
    return dtos



@pytest_asyncio.fixture
async def generate_events(
    create_event_model_dtos: list[CreateEventModelDto],
    async_client,
    user_with_token_model
) -> list[EventModel]:
    event_models = []
    headers = {"Authorization": f"Bearer {user_with_token_model.access_token}"}
    for dto in create_event_model_dtos:
        response = await async_client.post(
            "/v1/events/",
            json=dto.model_dump(by_alias=True, mode="json"),
            headers=headers,
        )
        event_models.append(EventModel(**response.json()))
    yield event_models
    for model in event_models:
        await async_client.delete(f"/v1/events/{model.id}", headers=headers)
