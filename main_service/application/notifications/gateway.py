from abc import ABCMeta, abstractmethod

from domain.notifications.entities import Notification
from domain.users.entities import User


class NotificationGateway(metaclass=ABCMeta):
    @abstractmethod
    async def send(
        self, notification: Notification, recipient: User
    ) -> Notification: ...
