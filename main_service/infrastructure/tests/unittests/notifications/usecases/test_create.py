from venv import create

import pytest
from application.notifications.usecases import (
    CreateNotificationUseCase,
    DeleteNotificationUseCase,
)
from domain.events.entities import Event
from domain.notifications.dtos import CreateNotificationDto


@pytest.mark.asyncio
@pytest.mark.skip
async def test_create_success(
    create_notification_usecase: CreateNotificationUseCase,
    create_notification_dto: CreateNotificationDto,
    get_admin_event: Event,
):
    # TODO: сделать мемберов для ивента
    notification = await create_notification_usecase(
        get_admin_event, create_notification_dto.send_date
    )
    attrs = (
        "recipient_id",
        "text",
        "type",
        "format",
        "status",
    )
    print(notification)
    for attr in attrs:
        assert getattr(notification, attr) == getattr(create_notification_dto, attr)
    assert notification.id == 1
