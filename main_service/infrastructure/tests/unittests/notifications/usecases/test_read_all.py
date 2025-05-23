import pytest
from application.notifications.usecases import ReadAllNotificationsUseCase
from domain.notifications.dtos import ReadNotificationsDto
from domain.notifications.entities import Notification


@pytest.mark.asyncio
async def test_read_all_success(
    read_all_notifications_usecase: ReadAllNotificationsUseCase,
    read_all_notifications_dto: ReadNotificationsDto,
    create_notification: Notification,
):
    notifications = await read_all_notifications_usecase(
        dto=read_all_notifications_dto
    )
    assert len(notifications) == 1
    assert notifications[0] == create_notification


@pytest.mark.asyncio
async def test_read_all_empty(
    read_all_notifications_usecase: ReadAllNotificationsUseCase,
    read_all_notifications_dto: ReadNotificationsDto,
):
    read_all_notifications_dto.page_size = 1
    read_all_notifications_dto.page = 2
    notifications = await read_all_notifications_usecase(
        dto=read_all_notifications_dto
    )
    assert len(notifications) == 0
