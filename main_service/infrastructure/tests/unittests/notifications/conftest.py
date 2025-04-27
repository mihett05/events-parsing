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
from domain.notifications.repositories import NotificationRepository


@pytest_asyncio.fixture
async def create_notification_dto() -> CreateNotificationDto:
    return CreateNotificationDto(
        recipient_id=1,
        text="Example",
        type=NotificationTypeEnum.EMAIL,
        format=NotificationFormatEnum.RAW_TEXT,
        status=NotificationStatusEnum.NO,
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
) -> NotificationRepository:
    async with container() as nested:
        yield await nested.get(NotificationRepository)


@pytest_asyncio.fixture
async def create_notification(
    create_notification_dto: CreateNotificationDto,
    notification_repository: NotificationRepository,
) -> Notification:
    return await notification_repository.create(create_notification_dto)
