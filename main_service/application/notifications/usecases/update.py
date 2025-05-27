from domain.notifications.entities import Notification
from domain.notifications.enums import NotificationStatusEnum
from domain.notifications.repositories import NotificationsRepository


class UpdateNotificationsStatusUseCase:
    """
    Сценарий массового обновления статусов уведомлений.

    Предоставляет бизнес-логику для изменения статусов
    группы уведомлений с сохранением изменений в хранилище.
    """

    def __init__(self, repository: NotificationsRepository):
        """
        Инициализация сценария обновления статусов.
        """
        self.__repository = repository

    async def __call__(
        self, notifications: list[Notification], status: NotificationStatusEnum
    ) -> list[Notification]:
        """
        Выполняет массовое(как теневое клонирование) обновление статусов уведомлений.
        """
        return await self.__repository.change_notifications_statuses(
            notifications, status
        )
