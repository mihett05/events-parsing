from domain.events.entities import EventUser
from domain.events.repositories import EventUsersRepository

from domain.users.entities import User

from application.transactions import TransactionsGateway


class CreateEventUserUseCase:
    def __init__(
        self,
        repository: EventUsersRepository,
        transaction: TransactionsGateway,
    ):
        self.__repository = repository
        self.__transaction = transaction

    async def __call__(self, event_id: int, actor: User) -> EventUser:
        async with self.__transaction:
            return await self.__repository.create(EventUser(event_id, actor.id))
