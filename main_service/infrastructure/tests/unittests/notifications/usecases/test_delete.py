import pytest
from application.notifications.usecases import (
    DeleteNotificationUseCase,
    ReadNotificationUseCase,
)
from domain.notifications.entities import Notification
from domain.notifications.exceptions import NotificationNotFoundError


@pytest.mark.asyncio
async def test_delete_success(
    create_notification: Notification,
    delete_notification_usecase: DeleteNotificationUseCase,
    read_notification_usecase: ReadNotificationUseCase,
):
    notification = await delete_notification_usecase(
        create_notification.id, None
    )
    assert notification == create_notification
    with pytest.raises(NotificationNotFoundError):
        await read_notification_usecase(notification.id)


@pytest.mark.asyncio
async def test_delete_not_found(
    delete_notification_usecase: DeleteNotificationUseCase,
):
    with pytest.raises(NotificationNotFoundError):
        await delete_notification_usecase(100500, None)
