from abc import ABCMeta, abstractmethod

import domain.notifications.dtos as dtos
import domain.notifications.entities as entities
import domain.notifications.enums as enums


class NotificationsRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(
        self, dto: dtos.CreateNotificationDto
    ) -> entities.Notification: ...

    @abstractmethod
    async def read(self, id_: int) -> entities.Notification: ...

    @abstractmethod
    async def read_all(
        self, dto: dtos.ReadNotificationsDto
    ) -> list[entities.Notification]: ...

    @abstractmethod
    async def change_notifications_statuses(
        self,
        notifications: list[entities.Notification],
        status: enums.NotificationStatusEnum,
    ): ...

    @abstractmethod
    async def delete(
        self, notification: entities.Notification
    ) -> entities.Notification: ...
