import json
from dataclasses import asdict

from application.events.coordinator.gateway import CoordinatorGateway
from domain.mails.entities import Mail
from faststream.rabbit import (
    ExchangeType,
    RabbitBroker,
    RabbitExchange,
    RabbitQueue,
)

exchange = RabbitExchange(
    "main",
    type=ExchangeType.TOPIC,
    auto_delete=False,
    durable=True,
)
queue = RabbitQueue(
    name="publish",
    durable=True,
    auto_delete=True,
    routing_key="events.mails",
)


class RabbitMQCoordinatorGateway(CoordinatorGateway):
    def __init__(self, broker: RabbitBroker):
        self.__broker = broker

    async def run(self, mails: list[Mail]):
        message = json.dumps(
            map(lambda x: asdict(x), mails),
            ensure_ascii=False,
        )

        await self.__broker.publish(message, queue=queue, exchange=exchange)
