import pytest
from application.notifications.usecases import CreateNotificationUseCase
from domain.notifications.dtos import CreateNotificationDto


@pytest.mark.asyncio
async def test_create_success(
    create_notification_usecase: CreateNotificationUseCase,
    create_notification_dto: CreateNotificationDto,
):
    # TODO: Переделать
    pass
