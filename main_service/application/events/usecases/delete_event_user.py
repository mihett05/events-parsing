from domain.events.entities import EventUser
from domain.events.repositories import EventUsersRepository
from domain.users.entities import User

from application.events.usecases.read_event_user import ReadEventUserUseCase
from application.transactions import TransactionsGateway


class DeleteEventUserUseCase:
    """UseCase для удаления связи пользователя с событием.

    Обеспечивает удаление связи пользователя с событием
    с предварительной проверкой существования связи
    и транзакционным выполнением операции.
    """

    def __init__(
        self,
        repository: EventUsersRepository,
        transaction: TransactionsGateway,
        read_use_case: ReadEventUserUseCase,
    ):
        """Инициализирует зависимости"""

        self.__repository = repository
        self.__transaction = transaction
        self.__use_case = read_use_case

    async def __call__(self, event_id: int, actor: User) -> EventUser:
        """Удаляет связь пользователя с событием."""

        async with self.__transaction:
            event_user = await self.__use_case(event_id, actor.id)
            print(event_user)
            return await self.__repository.delete(event_user)
