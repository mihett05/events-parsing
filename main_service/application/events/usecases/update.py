from domain.events.entities import Event
from domain.events.repositories import EventsRepository
from domain.users.entities import User

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.events.dtos import UpdateEventDto
from application.events.permissions import EventPermissionProvider
from application.events.usecases.read import ReadEventUseCase
from application.transactions import TransactionsGateway
from application.users.usecases import ReadUserRolesUseCase


class UpdateEventUseCase:
    def __init__(
        self,
        repository: EventsRepository,
        tx: TransactionsGateway,
        read_event_use_case: ReadEventUseCase,
        builder: PermissionBuilder,
        read_roles_use_case: ReadUserRolesUseCase,
    ):
        self.__repository = repository
        self.__transaction = tx
        self.__read_event_use_case = read_event_use_case
        self.__builder = builder
        self.__read_roles_use_case = read_roles_use_case

    async def __call__(self, dto: UpdateEventDto, actor: User | None) -> Event:
        async with self.__transaction:
            event = await self.__read_event_use_case(dto.event_id)
            roles = await self.__read_roles_use_case(actor.id)
            self.__builder.providers(
                EventPermissionProvider(event.organization_id, roles)
            ).add(
                PermissionsEnum.CAN_UPDATE_EVENT,
            ).apply()

            event.title = dto.title
            event.description = dto.description

            return await self.__repository.update(event)
