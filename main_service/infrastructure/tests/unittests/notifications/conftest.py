import pytest
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


@pytest_asyncio.fixture
async def create_notification_dto() -> CreateNotificationDto:
    return CreateNotificationDto(
        recipient_id=1,
        text="Example",
        type=NotificationTypeEnum.EMAIL,
        format=NotificationFormatEnum.RAW_TEXT,
        status=NotificationStatusEnum.UNSENT,
    )


@pytest_asyncio.fixture
async def read_all_notifications_dto() -> ReadNotificationsDto:
    return ReadNotificationsDto(
        page=0,
        page_size=50,
    )


@pytest_asyncio.fixture
async def notification_repository(
    container: AsyncContainer,
) -> NotificationsRepository:
    async with container() as nested:
        yield await nested.get(NotificationsRepository)


@pytest_asyncio.fixture
async def create_notification(
    create_notification_dto: CreateNotificationDto,
    notification_repository: NotificationsRepository,
) -> Notification:
    return await notification_repository.create(create_notification_dto)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare(
    pytestconfig: pytest.Config,
    notification_repository: OrganizationsRepository,
):
    if pytestconfig.getoption("--integration", default=False):
        return
    await notification_repository.clear()  # noqa
