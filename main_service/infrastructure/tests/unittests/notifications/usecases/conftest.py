import application.notifications.usecases as usecases
import pytest_asyncio
from dishka import AsyncContainer


@pytest_asyncio.fixture
async def create_notification_usecase(
    container: AsyncContainer,
) -> usecases.CreateNotificationUseCase:
    async with container() as nested:
        yield await nested.get(usecases.CreateNotificationUseCase)


@pytest_asyncio.fixture
async def read_notification_usecase(
    container: AsyncContainer,
) -> usecases.ReadNotificationUseCase:
    async with container() as nested:
        yield await nested.get(usecases.ReadNotificationUseCase)


@pytest_asyncio.fixture
async def read_all_notifications_usecase(
    container: AsyncContainer,
) -> usecases.ReadAllNotificationsUseCase:
    async with container() as nested:
        yield await nested.get(usecases.ReadAllNotificationsUseCase)


@pytest_asyncio.fixture
async def delete_notification_usecase(
    container: AsyncContainer,
) -> usecases.DeleteNotificationUseCase:
    async with container() as nested:
        yield await nested.get(usecases.DeleteNotificationUseCase)
