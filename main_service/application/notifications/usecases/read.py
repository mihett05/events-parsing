from domain.notifications.entities import Notification
from domain.notifications.repositories import NotificationsRepository


class ReadNotificationUseCase:
    def __init__(self, repository: NotificationsRepository):
        self.__repository = repository

    async def __call__(self, notification_id: int) -> Notification:
        return await self.__repository.read(notification_id)
