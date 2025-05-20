import pytest
from application.notifications.usecases import ReadNotificationUseCase
from domain.notifications.entities import Notification
from domain.notifications.exceptions import NotificationNotFoundError


@pytest.mark.asyncio
async def test_read_success(
    read_notification_usecase: ReadNotificationUseCase,
    create_notification,
        delete_notification_usecase,
):
    create_notification = await create_notification()
    notification = await read_notification_usecase(create_notification.id)
    assert notification == create_notification
    await delete_notification_usecase(notification.id, None)


@pytest.mark.asyncio
async def test_read_not_found(
    read_notification_usecase: ReadNotificationUseCase,
):
    with pytest.raises(NotificationNotFoundError):
        await read_notification_usecase(100500)
