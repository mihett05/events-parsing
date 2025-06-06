from datetime import datetime

from domain.notifications.dtos import ReadNotificationsDto
from domain.notifications.enums import NotificationStatusEnum

from ...transactions import TransactionsGateway
from ...users.usecases import ReadUsersByIdsUseCase
from .read_all import ReadAllNotificationsUseCase
from .send import SendNotificationsUseCase
from .update import UpdateNotificationsStatusUseCase


class ProcessUnsentNotificationsUseCase:
    """
    Юзкейс обработки неотправленных уведомлений.

    Оркестрирует процесс массовой отправки уведомлений, включая:
    - выборку неотправленных уведомлений
    - получение данных получателей
    - отправку через внешний сервис
    - обновление статусов уведомлений
    """

    def __init__(
        self,
        transaction: TransactionsGateway,
        read_users_by_ids: ReadUsersByIdsUseCase,
        read_all_notifications: ReadAllNotificationsUseCase,
        send_notifications: SendNotificationsUseCase,
        update_notifications_status: UpdateNotificationsStatusUseCase,
    ):
        """
        Инициализирует зависимости для работы с:
        - транзакциями
        - данными пользователей
        - выборкой уведомлений
        - сервисом отправки
        - обновлением статусов
        """

        self.__transaction = transaction

        self.__read_users_by_ids = read_users_by_ids
        self.__read_all_notifications = read_all_notifications
        self.__send_notifications = send_notifications
        self.__update_notifications_status = update_notifications_status

    async def __call__(self):
        """
        Основной метод обработки уведомлений.

        Выполняет в транзакции:
        - получение списка неотправленных уведомлений
        - отправку с разделением на успешные/неуспешные
        - фиксацию результатов отправки
        """

        dto = ReadNotificationsDto(
            page=0,
            page_size=50,
            send_date=datetime.now().date(),
            for_update=True,
        )

        async with self.__transaction:
            notifications = await self.__read_all_notifications(dto)
            user_ids = list(map(lambda x: x.recipient_id, notifications))
            users = {user.id: user for user in await self.__read_users_by_ids(user_ids)}

            failed, succeed = await self.__send_notifications(notifications, users)

            await self.__update_notifications_status(
                failed, NotificationStatusEnum.FAILED
            )
            await self.__update_notifications_status(
                succeed, NotificationStatusEnum.SENT
            )
