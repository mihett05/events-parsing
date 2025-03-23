from abc import ABCMeta, abstractmethod

import MainService.Domain.Notification.Dtos as dtos
import MainService.Domain.Notification.Entities as ent


class NotificationRepository(metaclass= ABCMeta):
    @abstractmethod
    async def create(self, dto: dtos.CreateNotificationDto) -> ent.Notification: ...
    @abstractmethod
    async def read(self, id_: int) -> ent.Notification: ...
    @abstractmethod
    async def read_all(self, dto: dtos.ReadNotificationsDto) -> list[ent.Notification]: ...
    @abstractmethod
    async def delete(self, notification: ent.Notification) -> ent.Notification: ...