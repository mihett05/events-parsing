from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.events.dtos import MakeSingleEventDto
from application.events.permissions import EventPermissionProvider
from application.events.usecases.read import ReadEventUseCase
from application.transactions import TransactionsGateway
from domain.events.entities import Event, EventSingle

from domain.events.repositories import EventsRepository
from domain.users.entities import User


class MakeSingleEventTypeUseCase:
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

    async def __call__(self, dto: MakeSingleEventDto, actor: User) -> Event:
        async with self.__transaction:
            event = await self.__read_use_case(dto.event_id)

            self.__builder.providers(EventPermissionProvider(event, actor)).add(
                PermissionsEnum.CAN_UPDATE_EVENT,
            ).apply()

            event_single = EventSingle(
                event_id=dto.event_id,
                start_date=dto.start_date,
                end_date=dto.end_date,
            )

            event.single = event_single
            event.repeatable = None

            await self.__repository.update(event)

        return event
