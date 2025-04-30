from domain.notifications.entities import Notification
from domain.notifications.enums import NotificationStatusEnum
from domain.notifications.repositories import NotificationsRepository


class UpdateManyNotificationUseCase:
    def __init__(self, repository: NotificationsRepository):
        self.__repository = repository

    async def __call__(
        self, notifications: list[Notification], status: NotificationStatusEnum
    ) -> list[Notification]:
        return await self.__repository.change_notifications_statuses(
            notifications, status
        )
