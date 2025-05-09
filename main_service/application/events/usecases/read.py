from domain.events.entities import Event
from domain.events.repositories import EventsRepository
from domain.users.entities import User

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.events.permissions import EventPermissionProvider
from application.transactions import TransactionsGateway
from application.users.usecases import ReadUserRolesUseCase


class ReadEventUseCase:
    def __init__(
        self,
        transaction: TransactionsGateway,
        repository: EventsRepository,
        builder: PermissionBuilder,
        read_roles_use_case: ReadUserRolesUseCase,
    ):
        self.__transaction = transaction
        self.__repository = repository
        self.__builder = builder
        self.__read_roles_use_case = read_roles_use_case

    async def __call__(self, event_id: int, actor: User) -> Event:
        async with self.__transaction:
            event = await self.__repository.read(event_id)
            roles = await self.__read_roles_use_case(actor.id)
            self.__builder.providers(
                EventPermissionProvider(event.organization_id, roles)
            ).add(
                PermissionsEnum.CAN_READ_EVENT,
            ).apply()
            return event
