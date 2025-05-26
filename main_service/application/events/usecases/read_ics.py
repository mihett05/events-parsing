from uuid import UUID

from domain.events.dtos import ReadUserEventsDto
from domain.events.entities import Event
from domain.events.repositories import EventsRepository

from application.events.usecases.read_for_user import ReadUserEventsUseCase
from application.transactions import TransactionsGateway
from application.users.usecases.read_by_calendar_uuid import ReadByCalendarUUIDUseCase


class ReadICSUseCase:
    def __init__(
        self,
        repository: EventsRepository,
        transaction: TransactionsGateway,
        user_use_case: ReadByCalendarUUIDUseCase,
        read_use_case: ReadUserEventsUseCase,
    ):
        self.__repository = repository
        self.__user_use_case = user_use_case
        self.__read_use_case = read_use_case
        self.__transaction = transaction

    async def __call__(self, uuid: UUID) -> list[Event]:
        async with self.__transaction:
            user = await self.__user_use_case(uuid)
            return await self.__read_use_case(ReadUserEventsDto(user.id))
