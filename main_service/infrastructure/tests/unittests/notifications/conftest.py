from typing import Callable, Coroutine, Any

import pytest
from datetime import datetime

import pytest_asyncio
from dishka import AsyncContainer
from domain.notifications.dtos import (
    CreateNotificationDto,
    ReadNotificationsDto,
)
from domain.notifications.entities import Notification
from domain.notifications.enums import (
    NotificationFormatEnum,
    NotificationStatusEnum,
    NotificationTypeEnum,
)
from domain.notifications.repositories import NotificationsRepository
from domain.organizations.repositories import OrganizationsRepository
from domain.users.repositories import UsersRepository


@pytest_asyncio.fixture
async def create_notification_dto(
    create_user1
) -> CreateNotificationDto:
    user = await create_user1()
    return CreateNotificationDto(
        recipient_id=user.id,
        text="Example",
        format=NotificationFormatEnum.RAW_TEXT,
        status=NotificationStatusEnum.UNSENT,
        event_id=1,
        send_date=datetime.now().date(),
    )


@pytest_asyncio.fixture
async def read_all_notifications_dto() -> ReadNotificationsDto:
    return ReadNotificationsDto(
        page=0, page_size=50, send_date=datetime.now().date(), for_update=True
    )


@pytest_asyncio.fixture
async def notification_repository(
    container: AsyncContainer,
) -> NotificationsRepository:
    async with container() as nested:
        yield await nested.get(NotificationsRepository)


@pytest_asyncio.fixture
async def users_repository(container: AsyncContainer) -> UsersRepository:
    async with container() as nested:
        yield await nested.get(UsersRepository)

@pytest_asyncio.fixture
async def orgatizations_repository(container: AsyncContainer) -> OrganizationsRepository:
    async with container() as nested:
        yield await nested.get(OrganizationsRepository)

@pytest_asyncio.fixture
async def create_notification(
    create_notification_dto: CreateNotificationDto,
    notification_repository: NotificationsRepository,
) -> Callable[..., Coroutine[Any, Any, Notification]]:
    async def _factory():
        return await notification_repository.create(create_notification_dto)
    return _factory

@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare(
    pytestconfig: pytest.Config,
    orgatizations_repository: OrganizationsRepository,
):
    if pytestconfig.getoption("--integration", default=False):
        return
    await orgatizations_repository.clear()  # noqa

@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare(
    pytestconfig: pytest.Config,
    notification_repository: NotificationsRepository,
):
    if pytestconfig.getoption("--integration", default=False):
        return
    await notification_repository.clear()  # noqa

@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare(
    pytestconfig: pytest.Config,
    users_repository: UsersRepository,
):
    if pytestconfig.getoption("--integration", default=False):
        return
    await users_repository.clear()  # noqa