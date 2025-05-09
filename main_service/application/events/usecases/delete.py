from domain.events.entities import Event
from domain.events.repositories import EventsRepository
from domain.users.entities import User

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.events.permissions import EventPermissionProvider
from application.events.usecases.read import ReadEventUseCase
from application.transactions import TransactionsGateway
from application.users.usecases import ReadUserRolesUseCase


class DeleteEventUseCase:
    def __init__(
        self,
        repository: EventsRepository,
        tx: TransactionsGateway,
        read_uc: ReadEventUseCase,
        builder: PermissionBuilder,
        read_roles_use_case: ReadUserRolesUseCase,
    ):
        self.__repository = repository
        self.__transaction = tx

        self.__read_use_case = read_uc
        self.__read_roles_use_case = read_roles_use_case
        self.__builder = builder

    async def __call__(self, event_id: int, actor: User | None) -> Event:
        async with self.__transaction:
            event = await self.__read_use_case(event_id)
            roles = await self.__read_roles_use_case(actor.id)
            self.__builder.providers(
                EventPermissionProvider(event.organization_id, roles)
            ).add(
                PermissionsEnum.CAN_DELETE_EVENT,
            ).apply()
            return await self.__repository.delete(event)
