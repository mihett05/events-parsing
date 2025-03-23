from application.events.dtos import UpdateEventDto
from application.events.usecases.check_permissions import CheckPermissionsUseCase
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
            check_uc: CheckPermissionsUseCase,
    ):
        self.__repository = repository
        self.__transaction = tx

        self.__read_use_case = read_uc
        self.__check_permissions_use_case = check_uc

    @staticmethod
    def set_model_attrs(event: Event, dto: UpdateEventDto) -> Event:
        ...

    async def __call__(self, dto: UpdateEventDto, actor: User) -> Event:
        async with self.__transaction as tx:
            event = await self.__read_use_case(dto.event_id)

            await self.__check_permissions_use_case(event, actor)

            self.set_model_attrs(event, dto)  # PS: it's plug
            await self.__repository.update(event)
            await tx.commit()

        return event
