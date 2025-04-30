from domain.notifications.dtos import ReadNotificationsDto
from domain.notifications.entities import Notification
from domain.notifications.enums import NotificationStatusEnum
from domain.notifications.exceptions import FailedSendNotificationError
from domain.notifications.repositories import NotificationsRepository

from ...users.usecases import ReadUsersByIdsUseCase
from ..factory import NotificationGatewayAbstractFactory
from .read_all import ReadAllNotificationsUseCase
from .update import UpdateManyNotificationUseCase


class SendNotificationsUseCase:
    def __init__(
        self,
        repository: NotificationsRepository,
        update_notification_use_case: UpdateManyNotificationUseCase,
        read_all_notification_use_case: ReadAllNotificationsUseCase,
        read_users_by_ids_use_case: ReadUsersByIdsUseCase,
        gateway_factory: NotificationGatewayAbstractFactory,
    ):
        self.__repository = repository
        self.__gateway_factory = gateway_factory
        self.__update_notification_use_case = update_notification_use_case
        self.__read_all_notification_use_case = read_all_notification_use_case
        self.__read_users_by_ids_use_case = read_users_by_ids_use_case

    async def __call__(self, dto: ReadNotificationsDto) -> list[Notification]:
        result = []
        dto = ReadNotificationsDto(page=0, page_size=50)
        while notifications := await self.__read_all_notification_use_case(dto):
            users = {
                user.id: user
                for user in await self.__read_users_by_ids_use_case(
                    list(map(lambda x: x.recipient_id, notifications))
                )
            }

            failed = []
            succeed = []
            for notification in notifications:
                gateway = await self.__gateway_factory.get(
                    users[notification.recipient_id]
                )
                try:
                    await gateway.send(
                        notification, users[notification.recipient_id]
                    )
                    notification.status = NotificationStatusEnum.SENT
                    succeed.append(notification)
                except FailedSendNotificationError:
                    notification.status = NotificationStatusEnum.FAILED
                    failed.append(notification)

            await self.__update_notification_use_case(
                failed, NotificationStatusEnum.FAILED
            )
            await self.__update_notification_use_case(
                succeed, NotificationStatusEnum.SENT
            )
            result.extend(notifications)

            dto.page += 1

        return result
