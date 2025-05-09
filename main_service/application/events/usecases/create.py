from domain.events.dtos import CreateEventDto
from domain.events.entities import Event
from domain.events.repositories import EventsRepository
from domain.users.entities import User

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.events.permissions import EventPermissionProvider
from application.users.usecases import ReadUserRolesUseCase


class CreateEventUseCase:
    def __init__(
        self,
        repository: EventsRepository,
        read_roles_use_case: ReadUserRolesUseCase,
        permission_builder: PermissionBuilder,
        transaction: TransactionsGatewa,
    ):
        self.__repository = repository
        self.__builder = permission_builder
        self.__transaction = transaction
        self.__read_roles_use_case = read_roles_use_case

    async def __call__(self, dto: CreateEventDto, actor: User) -> Event:
        async with self.__transaction:
            roles = await self.__read_roles_use_case(actor.id)
            self.__builder.providers(
                EventPermissionProvider(dto.organization_id, roles)
            ).add(PermissionsEnum.CAN_CREATE_EVENT).apply()
            return await self.__repository.create(dto)
