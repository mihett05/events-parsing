import shutil
from datetime import datetime
from typing import Iterable, Optional
from uuid import uuid4

import pytest_asyncio
import pytest
from dishka import AsyncContainer
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from infrastructure.api.app import create_app
from infrastructure.api.v1.attachments.models import AttachmentModel
from infrastructure.api.v1.auth.dtos import AuthenticateUserModelDto, CreateUserModelDto
from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.events.dtos import UpdateEventModelDto, CreateEventModelDto
from infrastructure.api.v1.events.models import EventModel
from infrastructure.api.v1.organizations.dtos import UpdateOrganizationModelDto, CreateOrganizationModelDto
from infrastructure.api.v1.organizations.models import OrganizationModel
from infrastructure.api.v1.users.dtos import UpdateUserModelDto
from infrastructure.api.v1.users.models import UserModel
from infrastructure.config import Config, get_config
from infrastructure.mocks.providers.container import (
    create_integration_test_container,
)


@pytest_asyncio.fixture
async def container() -> Iterable[AsyncContainer]:
    container = create_integration_test_container()
    yield container
    await container.close()


@pytest_asyncio.fixture
async def config() -> Config:
    return get_config()


@pytest_asyncio.fixture
async def get_app(container: AsyncContainer, config: Config):
    app = create_app(container, config)
    yield app
    shutil.rmtree("static")


@pytest_asyncio.fixture(autouse=True)
async def async_client(get_app: FastAPI) -> AsyncClient:
    transport = ASGITransport(app=get_app)
    async with AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        yield client


@pytest.fixture
def create_user_model_dto_factory() -> CreateUserModelDto:
    def _factory(
            email: str = "test@example.com",
            password: str = "password123",
            fullname: str = "Test User",
            is_active: bool = True,
    ) -> CreateUserModelDto:
        return CreateUserModelDto(
            email=email,
            password=password,
            fullname=fullname,
            isActive=is_active,
        )

    return _factory


@pytest.fixture
def authenticate_user_model_dto_factory() -> AuthenticateUserModelDto:
    def _factory(email: str = "test@example.com",
                 password: str = "password123") -> AuthenticateUserModelDto:
        return AuthenticateUserModelDto(email=email, password=password)

    return _factory


@pytest_asyncio.fixture
async def user_with_token_model_factory(
        user_model_factory,
        create_user_model_dto_factory,
        async_client) -> UserWithTokenModel:
    # def _factory(access_token: str = "fake-jwt-token",
    #              user: Optional[UserModel] = None) -> UserWithTokenModel:
    #     return UserWithTokenModel(accessToken=access_token,
    #                               user=user or user_model_factory())
    # return _factory

    response = await async_client.post(
        "/v1/auth/register",
        json=create_user_model_dto_factory().model_dump(by_alias=True, mode="json"),
    )
    model = UserWithTokenModel(**response.json())
    yield model
    await async_client.delete(
        "/v1/users/",
        headers={"Authorization": f"Bearer {model.access_token}"},
    )


# users.py

@pytest.fixture
def user_model_factory() -> UserModel:
    def _factory(
            id: int = 1,
            email: str = "test@example.com",
            fullname: str = "Test User",
            is_active: bool = True,
            telegram_id: int | None = None,
            created_at: datetime = datetime.now(),
    ) -> UserModel:
        return UserModel(
            id=id,
            email=email,
            fullname=fullname,
            isActive=is_active,
            telegramId=telegram_id,
            createdAt=created_at,
        )

    return _factory


@pytest.fixture
def update_user_model_dto_factory() -> UpdateUserModelDto:
    def _factory(fullname: str = "Updated Name",
                 telegram_id: int | None = 123456789) -> UpdateUserModelDto:
        return UpdateUserModelDto(fullname=fullname, telegramId=telegram_id)

    return _factory


# events.py
@pytest.fixture
def event_model_factory() -> EventModel:
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
def create_event_model_dto_factory() -> CreateEventModelDto:
    def _factory(
            title: str = "New Event",
            type_: str = "workshop",
            format_: str = "offline",
            location: Optional[str] = "Moscow",
            description: Optional[str] = "Some workshop",
            end_date: datetime = datetime(2025, 12, 31),
            start_date: datetime = datetime(2025, 12, 1),
            end_registration: datetime = datetime(2025, 11, 30),
            organization_id: int = 1,
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
            organizationId=organization_id,
        )

    return _factory


@pytest.fixture
def update_event_model_dto_factory() -> UpdateEventModelDto:
    def _factory(title: str = "Updated Title",
                 description: str = "Updated Description") -> UpdateEventModelDto:
        return UpdateEventModelDto(title=title, description=description)

    return _factory


# organizations.py
@pytest.fixture
def organization_model_factory() -> OrganizationModel:
    def _factory(
            id: int = 1,
            title: str = "Test Organization",
            created_at: datetime = datetime.now(),
            owner_id: int = 1,
    ) -> OrganizationModel:
        return OrganizationModel(id=id, title=title, created_at=created_at,
                                 ownerId=owner_id)

    return _factory


@pytest.fixture
def create_organization_model_dto_factory() -> CreateOrganizationModelDto:
    def _factory(title: str = "New Organization",
                 created_at: datetime = datetime.now()) -> CreateOrganizationModelDto:
        return CreateOrganizationModelDto(title=title, createdAt=created_at)

    return _factory


@pytest.fixture
def update_organization_model_dto_factory() -> UpdateOrganizationModelDto:
    def _factory(
            title: str = "Updated Organization Title") -> UpdateOrganizationModelDto:
        return UpdateOrganizationModelDto(title=title)

    return _factory


# attachments.py
@pytest.fixture
def attachment_model_factory() -> AttachmentModel:
    def _factory(
            filename: str = "test_file.jpg",
            extension: str = ".jpg",
            file_link: str = "http://example.com/files/test.jpg",
            mail_id: Optional[int] = None,
            event_id: Optional[int] = None,
    ) -> AttachmentModel:
        return AttachmentModel(
            id=uuid4(),
            filename=filename,
            extension=extension,
            fileLink=file_link,
            mailId=mail_id,
            eventId=event_id,
            createdAt=datetime.now(),
        )

    return _factory
