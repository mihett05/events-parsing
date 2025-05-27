from application.notifications.factory import NotificationGatewayAbstractFactory
from application.notifications.gateway import NotificationGateway
from domain.users.entities import User
from domain.users.enums import UserNotificationSendToEnum

from infrastructure.gateways.notifications.gateways.mail import (
    NotificationEmailGateway,
)
from infrastructure.gateways.notifications.gateways.telegram import (
    NotificationTelegramGateway,
)


class NotificationGatewayFactory(NotificationGatewayAbstractFactory):
    """
    Фабрика для получения шлюза уведомлений в зависимости от предпочтений пользователя.

    Предоставляет соответствующий шлюз (email или telegram) на основе настроек пользователя
    или переопределенного типа доставки.
    """

    def __init__(
        self,
        telegram: NotificationTelegramGateway,
        email: NotificationEmailGateway,
    ):
        self.__gateways = {
            UserNotificationSendToEnum.EMAIL: email,
            UserNotificationSendToEnum.TELEGRAM: telegram,
        }

    def get(
        self, user: User, *, override: UserNotificationSendToEnum = None
    ) -> NotificationGateway:
        """Возвращает шлюз уведомлений для указанного пользователя."""

        return self.__gateways[override or user.settings.type]
