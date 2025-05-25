from domain.events.dtos import ReadUserEventsDto
from domain.events.entities import EventUser
from domain.events.repositories import EventUsersRepository
from domain.users.entities import User

from application.transactions import TransactionsGateway


class ReadForUserEventUserUseCase:
    def __init__(
        self,
        repository: EventUsersRepository,
        transaction: TransactionsGateway,
    ):
        self.__repository = repository
        self.__transaction = transaction

    async def __call__(self, dto: ReadUserEventsDto, actor: User) -> list[EventUser]:
        async with self.__transaction:
            return await self.__repository.read_for_user(dto)
