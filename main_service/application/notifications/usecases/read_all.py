from domain.notifications.dtos import ReadNotificationsDto
from domain.notifications.entities import Notification
from domain.notifications.repositories import NotificationsRepository


class ReadAllNotificationsUseCase:
    """
    Юзкейс получения списка уведомлений по заданным критериям.

    Обеспечивает выборку уведомлений с возможностью фильтрации и пагинации.
    """

    def __init__(self, repository: NotificationsRepository):
        """
        Инициализирует репозиторий для работы с уведомлениями.
        """

        self.__repository = repository

    async def __call__(self, dto: ReadNotificationsDto) -> list[Notification]:
        """
        Возвращает список уведомлений, соответствующих параметрам выборки.
        """

        return await self.__repository.read_all(dto)
