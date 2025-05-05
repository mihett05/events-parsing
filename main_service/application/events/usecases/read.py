from domain.events.entities import Event
from domain.events.repositories import EventsRepository

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.events.permissions import EventPermissionProvider


class ReadEventUseCase:
    def __init__(
        self, repository: EventsRepository, builder: PermissionBuilder
    ):
        self.__repository = repository
        self.__builder = builder

    async def __call__(self, event_id: int) -> Event:
        event = await self.__repository.read(event_id)
        self.__builder.providers(
            EventPermissionProvider(event.organization_id, None)
        ).add(
            PermissionsEnum.CAN_READ_EVENT,
        ).apply()
        return event
