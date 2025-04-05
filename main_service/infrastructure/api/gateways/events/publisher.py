import json
from dataclasses import asdict

from faststream.rabbit import RabbitBroker, RabbitQueue

from application.events.coordinator.gateway import CoordinatorGateway
from domain.mails.entities import Mail
from infrastructure.config import Config


class RabbitMQCoordinatorGatewayPublisher(CoordinatorGateway):
    def __init__(self, broker: RabbitBroker, config: Config):
        self.__broker = broker
        self.__queue = RabbitQueue(config.default_publish_rabbitmq_queue)

    async def run(self, mails: list[Mail]):
        message = json.dumps(
            map(lambda x: asdict(x), mails),
            ensure_ascii=False,
        )

        await self.__broker.publish(message, self.__queue)
