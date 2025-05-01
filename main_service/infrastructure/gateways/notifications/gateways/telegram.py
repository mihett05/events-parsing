from aiogram import Bot
from application.notifications.gateway import NotificationGateway
from domain.notifications.entities import Notification
from domain.notifications.exceptions import FailedSendNotificationError
from domain.users.entities import User


class NotificationTelegramGateway(NotificationGateway):
    def __init__(self, bot: Bot):
        self.__bot = bot

    async def send(
        self, notification: Notification, recipient: User
    ) -> Notification:
        if recipient.telegram_id is None:
            raise FailedSendNotificationError
        try:
            await self.__bot.send_message(
                recipient.telegram_id, notification.text
            )
            return notification
        except Exception:
            raise FailedSendNotificationError
