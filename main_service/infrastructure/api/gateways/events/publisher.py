import json

from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue

from application.events.coordinator.gateway import CoordinatorGateway
from domain.mails.entities import Mail


class RabbitMQCoordinatorGatewayPublisher(CoordinatorGateway):
    def __init__(self, broker: RabbitBroker, exchange: str, queue: str):
        self.__broker = broker
        self.__exchange = RabbitExchange(exchange)
        self.__queue = RabbitQueue(queue)

    async def run(self, mails: list[Mail]):
        message = json.dumps(
            map(lambda x: x.asdict(), mails),
            ensure_ascii=False,
        )

        await self.__broker.publish(message, self.__queue, self.__exchange)
