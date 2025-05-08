from domain.notifications.entities import Notification
from domain.notifications.enums import NotificationStatusEnum
from domain.notifications.exceptions import FailedSendNotificationError
from domain.users.entities import User

from ..factory import NotificationGatewayAbstractFactory


class SendNotificationsUseCase:
    def __init__(self, gateways: NotificationGatewayAbstractFactory):
        self.__gateways = gateways

    async def __call__(self, notifications: list[Notification], users: dict[int, User]):
        # TODO: тут потом можно продумать механизм ролбека,
        #  то есть что делать с notification если мы отправили, но не смогли обновить базу
        #  как вариант, на стороне гетевея собирать бакет того, что надо отправить
        #  и только после подтверждения выполнять
        #  но вообще, такая ситуация маловероятна, так что можно забить

        failed = []
        succeed = []
        for notification in notifications:
            recipient = users[notification.recipient_id]
            gateway = await self.__gateways.get(recipient)
            try:
                await gateway.send(notification, recipient)
                notification.status = NotificationStatusEnum.SENT
                succeed.append(notification)
            except FailedSendNotificationError:
                notification.status = NotificationStatusEnum.FAILED
                failed.append(notification)

        return failed, succeed
