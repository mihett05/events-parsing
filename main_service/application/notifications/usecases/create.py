from domain.notifications.entities import Notification
from domain.notifications.repositories import NotificationRepository
from domain.notifications.dtos import CreateNotificationDto


class CreateNotificationUseCase:
    def __init__(self, repository: NotificationRepository):
        self.__repository = repository

    async def __call__(self, dto: CreateNotificationDto) -> Notification:
        return await self.__repository.create(dto)
