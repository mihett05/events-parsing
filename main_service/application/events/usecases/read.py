from domain.events.entities import Event
from domain.events.repositories import EventsRepository
from domain.users.entities import User
from domain.users.role_getter import RoleGetter

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.events.permissions import EventPermissionProvider
from application.transactions import TransactionsGateway


class ReadEventUseCase:
    def __init__(
        self,
        transaction: TransactionsGateway,
        repository: EventsRepository,
        builder: PermissionBuilder,
        role_getter: RoleGetter,
    ):
        self.__transaction = transaction
        self.__repository = repository
        self.__builder = builder
        self.__role_getter = role_getter

    async def __call__(self, event_id: int, actor: User) -> Event:
        async with self.__transaction:
            event = await self.__repository.read(event_id)
            actor_role = await self.__role_getter(actor, event.organization_id)
            self.__builder.providers(
                EventPermissionProvider(event.organization_id, actor_role)
            ).add(
                PermissionsEnum.CAN_READ_EVENT,
            ).apply()
            return event
