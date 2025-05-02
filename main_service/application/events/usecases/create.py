from domain.events.dtos import CreateEventDto
from domain.events.entities import Event
from domain.events.repositories import EventsRepository
from domain.users.entities import User

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.events.permissions import EventPermissionProvider


class CreateEventUseCase:
    def __init__(
        self,
        repository: EventsRepository,
        builder: PermissionBuilder,
    ):
        self.__repository = repository
        self.__builder = builder

    async def __call__(self, dto: CreateEventDto, actor: User | None) -> Event:
        event = await self.__repository.create(dto)
        self.__builder.providers(EventPermissionProvider(event, actor)).add(
            PermissionsEnum.CAN_UPDATE_EVENT,
        ).apply()
        return event
