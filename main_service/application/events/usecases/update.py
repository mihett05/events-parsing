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

    @staticmethod
    def set_model_attrs(event: Event, dto: UpdateEventDto):
        event.type = dto.title
        event.members = dto.members

    async def __call__(self, dto: UpdateEventDto, actor: User) -> Event:
        async with self.__transaction:
            event = await self.__read_use_case(dto.event_id)

            self.__builder.providers(EventPermissionProvider(event, actor)).add(
                PermissionsEnum.CAN_UPDATE_EVENT,
            ).apply()

            self.set_model_attrs(event, dto)  # PS: it's plug
            await self.__repository.update(event)

        return event
