from application.events.dtos import MakeRepeatableEventDto
from application.events.usecases.check_permissions import CheckPermissionsUseCase
from application.events.usecases.read import ReadEventUseCase
from application.transactions import TransactionsGateway
from domain.events.entities import Event, EventRepeatable

from domain.events.repositories import EventsRepository
from domain.users.entities import User


class MakeRepeatableEventTypeUseCase:
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

    async def __call__(self, dto: MakeRepeatableEventDto, actor: User) -> Event:
        async with self.__transaction as tx:
            event = await self.__read_use_case(dto.event_id)

            await self.__check_permissions_use_case(event, actor)

            event_single = EventRepeatable(
                event_id=dto.event_id,
                start_time=dto.start_time,
                end_time=dto.end_time,
                start_day=dto.start_day,
                end_day=dto.end_day,
            )

            event.single = event_single
            event.repeatable = None

            await self.__repository.update(event)
            await tx.commit()

        return event
