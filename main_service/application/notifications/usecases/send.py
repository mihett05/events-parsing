from domain.notifications.dtos import ReadNotificationsDto
from domain.notifications.entities import Notification
from domain.notifications.enums import NotificationStatusEnum
from domain.notifications.exceptions import FailedSendNotificationError

from ...users.usecases import ReadUsersByIdsUseCase
from ..factory import NotificationGatewayAbstractFactory
from .read_all import ReadAllNotificationsUseCase
from .update import UpdateNotificationsStatusUseCase


class SendNotificationsUseCase:
    def __init__(
        self,
        gateways: NotificationGatewayAbstractFactory,
        read_users_by_ids: ReadUsersByIdsUseCase,
        read_all_notifications: ReadAllNotificationsUseCase,
        update_notifications_status: UpdateNotificationsStatusUseCase,
    ):
        self.__gateways = gateways

        self.__read_users_by_ids = read_users_by_ids
        self.__read_all_notifications = read_all_notifications
        self.__update_notifications_status = update_notifications_status

    async def __call__(self, dto: ReadNotificationsDto):
        dto = ReadNotificationsDto(page=0, page_size=50)
        while notifications := await self.__read_all_notifications(dto):
            await self.__send_bucket(notifications)
            dto.page += 1

    async def __send_bucket(self, notifications: list[Notification]):
        # TODO: тут потом можно продумать механизм ролбека,
        #  то есть что делать с notification если мы отправили, но не смогли обновить базу
        #  как вариант, на стороне гетевея собирать бакет того, что надо отправить
        #  и только после подтверждения выполнять
        #  но вообще, такая ситуация маловероятна, так что можно забить

        user_ids = list(map(lambda x: x.recipient_id, notifications))
        users = {user.id: user for user in await self.__read_users_by_ids(user_ids)}

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

        await self.__update_notifications_status(failed, NotificationStatusEnum.FAILED)
        await self.__update_notifications_status(succeed, NotificationStatusEnum.SENT)
