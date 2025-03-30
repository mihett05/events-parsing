from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.events.dtos import UpdateEventDto
from application.events.permissions import EventPermissionProvider
from application.events.usecases.read import ReadEventUseCase
from application.transactions import TransactionsGateway
from domain.events.entities import Event

from domain.events.repositories import EventsRepository
from domain.users.entities import User


class UpdateEventUseCase:
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

    async def __call__(self, dto: UpdateEventDto, actor: User | None) -> Event:
        async with self.__transaction:
            event = await self.__read_use_case(dto.event_id)

            self.__builder.providers(EventPermissionProvider(event, actor)).add(
                PermissionsEnum.CAN_UPDATE_EVENT,
            ).apply()

            event.title = dto.title
            event.description = dto.description
            # event.members = dto.members

            await self.__repository.update(event)

        return event
