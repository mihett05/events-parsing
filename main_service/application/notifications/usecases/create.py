from domain.notifications.dtos import CreateNotificationDto
from domain.notifications.entities import Notification
from domain.notifications.repositories import NotificationsRepository


class CreateNotificationUseCase:
    def __init__(self, repository: NotificationsRepository):
        self.__repository = repository

    async def __call__(self, dto: CreateNotificationDto) -> Notification:
        return await self.__repository.create(dto)
