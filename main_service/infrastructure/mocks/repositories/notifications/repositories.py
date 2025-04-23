from datetime import datetime, timezone

from domain.notifications.entities import Notification
from domain.notifications.dtos import (
    CreateNotificationDto,
    ReadNotificationsDto,
)
from domain.notifications.exceptions import (
    NotificationNotFoundError,
    NotificationAlreadyExistsError,
)
from domain.notifications.repositories import NotificationRepository

from ..crud import Id, MockRepository, MockRepositoryConfig
from .mappers import map_create_dto_to_entity


class NotificationMemoryRepository(NotificationRepository):
    class Config(MockRepositoryConfig):
        def __init__(self):
            super().__init__(
                entity=Notification,
                not_found_exception=NotificationNotFoundError,
                already_exists_exception=NotificationAlreadyExistsError,
            )

        def extract_id(self, entity: Notification) -> Id:
            return entity.id

    def __init__(self):
        self.__next_id = 1
        self.__repository = MockRepository(self.Config())

    async def create(self, dto: CreateNotificationDto) -> Notification:
        notification = map_create_dto_to_entity(dto)
        notification.id = self.__next_id
        notification.created_at = datetime.now()
        self.__next_id += 1
        return await self.__repository.create(notification)

    async def read(self, notification_id: int) -> Notification:
        return await self.__repository.read(notification_id)

    async def read_all(self, dto: ReadNotificationsDto) -> list[Notification]:
        data = await self.__repository.read_all()
        return data[dto.page * dto.page_size : (dto.page + 1) * dto.page_size]

    async def delete(self, notification: Notification) -> Notification:
        return await self.__repository.delete(notification)
