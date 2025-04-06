from dishka import AsyncContainer
from faststream.rabbit import RabbitBroker, RabbitQueue

from application.events.dtos import EventInfo
from application.events.usecases import DeduplicateEventUseCase
from infrastructure.api.gateways.events.mappers import (
    map_event_info_from_pydantic,
)
from infrastructure.api.gateways.events.models import EventInfoModel
from infrastructure.config import Config


class RabbitMQCoordinatorGatewaySubscriber:
    def __init__(
            self,
            broker: RabbitBroker,
            config: Config,
            container: AsyncContainer,
    ):
        self.__broker = broker
        self.__queue = RabbitQueue(config.default_subscribe_rabbitmq_queue)
        self.__container = container

        self.__broker.subscriber(self.__queue)(self.receive)

    async def receive(self, message: str):
        dto: EventInfo = map_event_info_from_pydantic(
            EventInfoModel.model_validate_json(message)
        )
        async with self.__container() as request_container:
            deduplicate = await request_container.get(DeduplicateEventUseCase)
            return await deduplicate(dto)
