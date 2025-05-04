import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Coroutine, Optional

import pytest
import pytest_asyncio
from dishka import AsyncContainer
from domain.events.enums import EventFormatEnum, EventTypeEnum
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.events.dtos import (
    CreateEventModelDto,
    UpdateEventModelDto,
)
from infrastructure.api.v1.events.models import EventModel


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
        format_: EventFormatEnum = EventFormatEnum.OTHER,
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
def update_event_model_dto_factory(
    random_string_factory,
) -> Callable[[], UpdateEventModelDto]:
    def _factory(
        title: str = random_string_factory(10),
        description: str = random_string_factory(100),
    ) -> UpdateEventModelDto:
        return UpdateEventModelDto(title=title, description=description)

    return _factory


@pytest_asyncio.fixture
async def create_event_model_dtos(
    async_client: AsyncClient,
    create_event_model_dto_factory: Callable[..., CreateEventModelDto],
    random_string_factory,
) -> list[CreateEventModelDto]:
    dtos = []
    response = await async_client.get("/v1/organizations/")
    orgs = response.json()
    for i in range(10):
        date = datetime(2020, 1, 1)
        start_date = date + timedelta(days=random.randint(0, 2000))
        org = random.choice(orgs)
        dtos.append(
            create_event_model_dto_factory(
                title=f"{random_string_factory(10)}",
                organization_id=org["id"],
                start_date=start_date,
                end_date=start_date + timedelta(days=random.randint(0, 7)),
            )
        )
    return dtos


@pytest_asyncio.fixture
async def generate_events(
    create_event_model_dtos: list[CreateEventModelDto],
    async_client,
    user_with_token_model: Callable[..., Coroutine[Any, Any, UserWithTokenModel]],
) -> list[EventModel]:
    event_models = []
    user_with_token = await user_with_token_model()
    headers = {"Authorization": f"Bearer {user_with_token.access_token}"}
    for dto in create_event_model_dtos:
        response = await async_client.post(
            "/v1/events/",
            json=dto.model_dump(by_alias=True, mode="json"),
            headers=headers,
        )
        event_models.append(EventModel(**response.json()))
    yield event_models


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_organizations(container: AsyncContainer):
    base_path = Path(__file__).parent.parent.parent.parent.parent.parent.resolve()
    with open(base_path / "scripts/sql/insert_user.sql", encoding="utf8") as insert_organizations:
        insert_user_statement = insert_organizations.read()
    with open(
        base_path / "scripts/sql/insert_organizations.sql", encoding="utf8"
    ) as insert_organizations:
        insert_organizations_statement = insert_organizations.read()

    engine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        user_id = (await conn.execute(text(insert_user_statement))).scalar()
        await conn.execute(text(insert_organizations_statement.format(user_id=user_id)))
