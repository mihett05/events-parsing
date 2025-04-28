from domain.notifications.dtos import ReadNotificationsDto
from domain.notifications.entities import Notification
from domain.notifications.repositories import NotificationsRepository


class ReadAllNotificationsUseCase:
    def __init__(self, repository: NotificationsRepository):
        self.__repository = repository

    async def __call__(self, dto: ReadNotificationsDto) -> list[Notification]:
        return await self.__repository.read_all(dto)
