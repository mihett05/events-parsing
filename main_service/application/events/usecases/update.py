from domain.events.entities import Event
from domain.events.repositories import EventsRepository
from domain.users.entities import User
from domain.users.role_getter import RoleGetter

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.events.dtos import UpdateEventDto
from application.events.permissions import EventPermissionProvider
from application.events.usecases.read import ReadEventUseCase
from application.transactions import TransactionsGateway


class UpdateEventUseCase:
    def __init__(
        self,
        repository: EventsRepository,
        tx: TransactionsGateway,
        read_event_use_case: ReadEventUseCase,
        builder: PermissionBuilder,
        role_getter: RoleGetter,
    ):
        self.__repository = repository
        self.__transaction = tx
        self.__read_event_use_case = read_event_use_case
        self.__builder = builder
        self.__role_getter = role_getter

    async def __call__(self, dto: UpdateEventDto, actor: User) -> Event:
        async with self.__transaction:
            event = await self.__read_event_use_case(dto.event_id, actor)
            actor_roles = await self.__role_getter(actor, event.organization_id)
            self.__builder.providers(
                EventPermissionProvider(event.organization_id, actor_roles)
            ).add(
                PermissionsEnum.CAN_UPDATE_EVENT,
            ).apply()

            event.title = dto.title
            event.description = dto.description
            if dto.is_visible_status:
                event.is_visible = dto.is_visible_status
            return await self.__repository.update(event)
