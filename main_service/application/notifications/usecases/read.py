from domain.notifications.entities import Notification
from domain.notifications.repositories import NotificationsRepository


class ReadNotificationUseCase:
    """
    Юзкейс получения уведомления по идентификатору.

    Обеспечивает чтение данных конкретного уведомления из хранилища.
    """

    def __init__(self, repository: NotificationsRepository):
        """
        Инициализирует репозиторий для работы с уведомлениями.
        """

        self.__repository = repository

    async def __call__(self, notification_id: int) -> Notification:
        """
        Возвращает уведомление с указанным идентификатором.
        """
        return await self.__repository.read(notification_id)
