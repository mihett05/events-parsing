from abc import ABCMeta, abstractmethod

from domain.notifications.entities import Notification
from domain.users.entities import User


class NotificationGateway(metaclass=ABCMeta):
    @abstractmethod
    async def send(
        self, notification: Notification, recipient: User
    ) -> Notification: ...
    @abstractmethod
    async def __aenter__(self) -> "NotificationGateway": ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...
