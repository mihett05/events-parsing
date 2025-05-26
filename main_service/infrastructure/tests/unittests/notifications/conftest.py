from datetime import datetime
from typing import Any, Callable, Coroutine

import pytest
import pytest_asyncio
from dishka import AsyncContainer
from domain.events.entities import Event
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
from domain.users.entities import User
from domain.users.repositories import UsersRepository


@pytest_asyncio.fixture
async def create_notification_dto(
    get_user_entity: User, get_admin_event: Event
) -> CreateNotificationDto:
    return CreateNotificationDto(
        recipient_id=get_user_entity.id,
        text="Example",
        format=NotificationFormatEnum.RAW_TEXT,
        status=NotificationStatusEnum.UNSENT,
        event_id=get_admin_event.id,
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
async def orgatizations_repository(
    container: AsyncContainer,
) -> OrganizationsRepository:
    async with container() as nested:
        yield await nested.get(OrganizationsRepository)


@pytest_asyncio.fixture
async def create_notification(
    create_notification_dto: CreateNotificationDto,
    notification_repository: NotificationsRepository,
) -> Notification:
    return await notification_repository.create(create_notification_dto)
