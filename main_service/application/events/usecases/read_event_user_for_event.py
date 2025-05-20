from domain.events.dtos import ReadEventUsersDto
from domain.events.entities import EventUser
from domain.events.repositories import EventUsersRepository
from domain.users.entities import User

from application.transactions import TransactionsGateway


class ReadForEventEventUserUseCase:
    def __init__(
        self,
        repository: EventUsersRepository,
        transaction: TransactionsGateway,
    ):
        self.__repository = repository
        self.__transaction = transaction

    async def __call__(
        self, dto: ReadEventUsersDto, actor: User
    ) -> list[EventUser]:
        async with self.__transaction:
            return await self.__repository.read_for_event(dto)
