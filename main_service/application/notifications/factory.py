from abc import ABCMeta, abstractmethod

from domain.users.entities import User
from domain.users.enums import UserNotificationSendToEnum

from application.notifications.gateway import NotificationGateway


class NotificationGatewayAbstractFactory(metaclass=ABCMeta):
    @abstractmethod
    def get(
        self, user: User, *, override: UserNotificationSendToEnum = None
    ) -> NotificationGateway: ...
