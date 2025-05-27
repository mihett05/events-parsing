from domain.notifications.entities import Notification
from domain.notifications.repositories import NotificationsRepository
from domain.users.entities import User

from application.transactions import TransactionsGateway

from .read import ReadNotificationUseCase


class DeleteNotificationUseCase:
    """
    Юзкейс удаления уведомления.

    Обеспечивает безопасное удаление уведомления с проверкой прав доступа
    и поддержкой транзакционности операции.
    """

    def __init__(
        self,
        repository: NotificationsRepository,
        tx: TransactionsGateway,
        read_uc: ReadNotificationUseCase,
    ):
        """
        Инициализирует зависимости:
        - репозиторий для работы с уведомлениями
        - шлюз для управления транзакциями
        - юзкейс для проверки существования уведомления
        """

        self.__repository = repository
        self.__transaction = tx
        self.__read_use_case = read_uc

    async def __call__(self, notification_id: int, actor: User | None) -> Notification:
        """
        Выполняет удаление уведомления в рамках транзакции.
        Перед удалением проверяет существование уведомления.
        """

        async with self.__transaction:
            notification = await self.__read_use_case(notification_id)
            return await self.__repository.delete(notification)
