import pytest

from application.notifications.usecases import CreateNotificationUseCase
from domain.notifications.dtos import CreateNotificationDto


@pytest.mark.asyncio
async def test_create_success(
    create_notification_usecase: CreateNotificationUseCase,
    create_notification_dto: CreateNotificationDto,
):
    notification = await create_notification_usecase(
        dto=create_notification_dto
    )
    attrs = (
        "recipient_id",
        "text",
        "type",
        "format",
        "status",
    )
    for attr in attrs:
        assert getattr(notification, attr) == getattr(
            create_notification_dto, attr
        )
    assert notification.id == 1
