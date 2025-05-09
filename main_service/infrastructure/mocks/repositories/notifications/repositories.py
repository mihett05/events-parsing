from datetime import datetime

from domain.notifications.dtos import (
    CreateNotificationDto,
    ReadNotificationsDto,
)
from domain.notifications.entities import Notification
from domain.notifications.enums import NotificationStatusEnum
from domain.notifications.exceptions import (
    NotificationAlreadyExistsError,
    NotificationNotFoundError,
)
from domain.notifications.repositories import NotificationsRepository

from ..crud import Id, MockRepository, MockRepositoryConfig
from .mappers import map_create_dto_to_entity


class NotificationsMemoryRepository(NotificationsRepository):
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

    async def create_many(
        self, notifications: list[Notification]
    ) -> list[Notification]:
        result = []
        for notification in notifications:
            notification.id = self.__next_id
            notification.created_at = datetime.now()

            result.append(await self.__repository.create(notification))
            self.__next_id += 1

        return result

    async def read(self, notification_id: int) -> Notification:
        return await self.__repository.read(notification_id)

    async def read_all(self, dto: ReadNotificationsDto) -> list[Notification]:
        data: list[Notification] = await self.__repository.read_all()
        return [item for item in data if item.event_id]

    async def change_notifications_statuses(
        self, notifications: list[Notification], status: NotificationStatusEnum
    ):
        for notification in notifications:
            notification.status = status
            await self.__repository.update(notification)

    async def delete(self, notification: Notification) -> Notification:
        return await self.__repository.delete(notification)
