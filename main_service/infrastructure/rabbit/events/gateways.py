import asyncio

from application.events.coordinator.gateway import CoordinatorGateway
from domain.mails.entities import Mail
from faststream.rabbit import (
    ExchangeType,
    RabbitBroker,
    RabbitExchange,
    RabbitQueue,
)

from .mappers import map_mail_to_pydantic

exchange = RabbitExchange(
    "main",
    type=ExchangeType.TOPIC,
    auto_delete=False,
    durable=True,
)
queue = RabbitQueue(
    name="process-mails",
    durable=True,
    auto_delete=True,
    routing_key="events.mails",
)


class RabbitMQCoordinatorGateway(CoordinatorGateway):
    """Шлюз для координации событий через RabbitMQ."""

    def __init__(self, broker: RabbitBroker):
        """Инициализирует шлюз с подключением к брокеру сообщений."""

        self.__broker = broker

    async def run(self, mails: list[Mail]):
        """Асинхронно публикует список писем в очередь обработки."""

        await asyncio.gather(
            *[
                self.__broker.publish(
                    map_mail_to_pydantic(mail), queue=queue, exchange=exchange
                )
                for mail in mails
            ]
        )
