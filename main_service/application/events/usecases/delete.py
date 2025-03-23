from application.events.usecases.check_permissions import CheckPermissionsUseCase
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
            check_uc: CheckPermissionsUseCase,
    ):
        self.__repository = repository
        self.__transaction = tx

        self.__read_use_case = read_uc
        self.__check_permissions_use_case = check_uc

    async def __call__(self, event_id: int, actor: User) -> Event:
        async with self.__transaction as tx:
            event = await self.__read_use_case(event_id)

            await self.__check_permissions_use_case(event, actor)

            await self.__repository.delete(event)
            await tx.commit()

        return event
