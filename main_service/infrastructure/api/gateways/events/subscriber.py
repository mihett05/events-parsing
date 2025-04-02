from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue

from application.events.dtos import EventInfo
from application.events.usecases import FindEventUseCase, CreateEventUseCase
from application.mails.dtos import UpdateMailDto
from application.mails.usecases import ReadMailUseCase, UpdateMailUseCase
from domain.events.dtos import CreateEventDto
from domain.events.entities import Event
from domain.mails.enums import MailStateEnum
from infrastructure.api.gateways.events.mappers import (
    map_event_info_from_pydantic,
)
from infrastructure.api.gateways.events.models import EventInfoModel


class RabbitMQCoordinatorGatewaySubscriber:
    def __init__(
            self,
            mail_read_use_case: ReadMailUseCase,
            mail_update_use_case: UpdateMailUseCase,
            event_find_use_case: FindEventUseCase,
            event_create_use_case: CreateEventUseCase,
            broker: RabbitBroker,
            exchange: str,
            queue: str,
    ):
        self.__broker = broker
        self.__exchange = RabbitExchange(exchange)
        self.__queue = RabbitQueue(queue)

        self.mail_read_use_case = mail_read_use_case
        self.mail_update_use_case = mail_update_use_case
        self.event_find_use_case = event_find_use_case
        self.event_create_use_case = event_create_use_case

        self.__broker.subscriber(self.__queue, self.__exchange)(self.receive)

    async def receive(self, message: str):
        dto: EventInfo = map_event_info_from_pydantic(
            EventInfoModel.model_validate_json(message)
        )
        event: Event | None = await self.event_find_use_case(dto)

        if event is None:
            create_dto = CreateEventDto(
                title=dto.title or '',
                description=dto.description or '',
                organization_id=-1,
                end_date=dto.dates.end_date,
                start_date=dto.dates.start_date,
                end_registration=dto.dates.end_registration,
            )
            event: Event = await self.event_create_use_case(create_dto)

        await self.mail_update_use_case(
            UpdateMailDto(
                id=dto.mail_id,
                state=MailStateEnum.PROCESSED,
                event_id=event.id,
            )
        )
