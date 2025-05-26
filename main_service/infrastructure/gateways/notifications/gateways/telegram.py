from aiogram import Bot
from aiogram.enums import ParseMode
from application.notifications.gateway import NotificationGateway
from domain.notifications.entities import Notification
from domain.notifications.enums import NotificationFormatEnum
from domain.notifications.exceptions import FailedSendNotificationError
from domain.users.entities import User


class NotificationTelegramGateway(NotificationGateway):
    async def __aenter__(self) -> "NotificationGateway":
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    def __init__(self, bot: Bot):
        self.__bot = bot
        self.__mapper = {
            NotificationFormatEnum.RAW_TEXT: None,
            NotificationFormatEnum.HTML: ParseMode.HTML,
            NotificationFormatEnum.MARKDOWN: ParseMode.MARKDOWN,
        }

    async def send(self, notification: Notification, recipient: User) -> Notification:
        if recipient.telegram_id is None:
            raise FailedSendNotificationError

        try:
            await self.__bot.send_message(
                chat_id=recipient.telegram_id,
                text=notification.text,
                parse_mode=self.__mapper[notification.format],
            )
            return notification
        except Exception:
            raise FailedSendNotificationError
