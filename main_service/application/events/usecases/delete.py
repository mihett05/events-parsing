from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.events.permissions import EventPermissionProvider
from application.events.usecases.read import ReadEventUseCase
from application.transactions import TransactionsGateway
from domain.events.entities import Event

from domain.events.repositories import EventsRepository
from domain.users.entities import User


class DeleteEventUseCase:
    def __init__(
        self,
        repository: EventsRepository,
        tx: TransactionsGateway,
        read_uc: ReadEventUseCase,
        builder: PermissionBuilder,
    ):
        self.__repository = repository
        self.__transaction = tx

        self.__read_use_case = read_uc
        self.__builder = builder

    async def __call__(self, event_id: int, actor: User) -> Event:
        async with self.__transaction:
            event = await self.__read_use_case(event_id)

            self.__builder.providers(EventPermissionProvider(event, actor)).add(
                PermissionsEnum.CAN_DELETE_EVENT,
            ).apply()

            await self.__repository.delete(event)

        return event
