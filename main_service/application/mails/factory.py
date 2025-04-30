from abc import ABCMeta, abstractmethod

from domain.users.entities import User

from application.notifications.gateway import NotificationGateway


class NotificationGatewayFactory(metaclass=ABCMeta):
    @abstractmethod
    async def get(self, user: User) -> NotificationGateway: ...
