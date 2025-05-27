from abc import ABCMeta, abstractmethod

from domain.users.entities import User
from domain.users.enums import UserNotificationSendToEnum

from application.notifications.gateway import NotificationGateway


class NotificationGatewayAbstractFactory(metaclass=ABCMeta):
    """
    Абстрактная фабрика для получения шлюзов отправки уведомлений.

    Определяет интерфейс для получения конкретной реализации шлюза
    отправки уведомлений в зависимости от пользователя и его настроек.
    """

    @abstractmethod
    def get(
        self, user: User, *, override: UserNotificationSendToEnum = None
    ) -> NotificationGateway: ...

    """
    Возвращает шлюз отправки уведомлений для указанного пользователя.
    """
