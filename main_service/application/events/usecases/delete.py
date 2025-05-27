from domain.events.entities import Event
from domain.events.repositories import EventsRepository
from domain.users.entities import User
from domain.users.role_getter import RoleGetter

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.events.permissions import EventPermissionProvider
from application.events.usecases.read import ReadEventUseCase
from application.transactions import TransactionsGateway


class DeleteEventUseCase:
    """UseCase для удаления события.

    Реализует безопасное удаление события с проверкой прав доступа
    и транзакционным выполнением операции.
    """

    def __init__(
        self,
        repository: EventsRepository,
        tx: TransactionsGateway,
        read_uc: ReadEventUseCase,
        builder: PermissionBuilder,
        role_getter: RoleGetter,
    ):
        """Инициализирует зависимости"""

        self.__repository = repository
        self.__transaction = tx
        self.__read_use_case = read_uc
        self.__role_getter = role_getter
        self.__builder = builder

    async def __call__(self, event_id: int, actor: User) -> Event:
        """Удаляет событие с проверкой прав."""
        async with self.__transaction:
            event = await self.__read_use_case(event_id, actor)
            actor_role = await self.__role_getter(actor, event.organization_id)
            self.__builder.providers(
                EventPermissionProvider(event.organization_id, actor_role)
            ).add(
                PermissionsEnum.CAN_DELETE_EVENT,
            ).apply()
            return await self.__repository.delete(event)
