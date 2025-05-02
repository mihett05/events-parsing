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
    def __init__(
        self,
        telegram: NotificationTelegramGateway,
        email: NotificationEmailGateway,
    ):
        self.strategy = {
            UserNotificationSendToEnum.EMAIL: email,
            UserNotificationSendToEnum.TELEGRAM: telegram,
        }

    async def get(self, user: User) -> NotificationGateway:
        return self.strategy[user.settings.type]
