from abc import ABCMeta, abstractmethod

from domain.notifications.entities import Notification
from domain.users.entities import User


class NotificationGateway(metaclass=ABCMeta):
    """
    Абстрактный шлюз для отправки уведомлений.

    Определяет базовый интерфейс для всех реализаций шлюзов отправки уведомлений,
    включая поддержку асинхронного контекстного менеджера.
    """

    @abstractmethod
    async def send(
        self, notification: Notification, recipient: User
    ) -> Notification: ...

    """
    Отправляет уведомление указанному получателю.
    """

    @abstractmethod
    async def __aenter__(self) -> "NotificationGateway": ...
    """
    Вход в асинхронный контекстный менеджер.
    """

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    """
    Выход из асинхронного контекстного менеджера.
    """
