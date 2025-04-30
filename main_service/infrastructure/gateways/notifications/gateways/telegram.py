from application.notifications.gateway import NotificationGateway
from domain.notifications.entities import Notification
from domain.users.entities import User


class NotificationTelegramGateway(NotificationGateway):
    async def send(
        self, notification: Notification, recipient: User
    ) -> Notification:
        raise NotImplementedError
