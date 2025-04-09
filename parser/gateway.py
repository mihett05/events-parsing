import logging
from dataclasses import asdict
from datetime import datetime
from parser.config import get_config
from parser.events import DatesInfo, EventInfo
from parser.pipeline import pipeline

from faststream import Depends, FastStream
from faststream.rabbit import (
    ExchangeType,
    RabbitBroker,
    RabbitExchange,
    RabbitQueue,
)

config = get_config()
broker = RabbitBroker(config.rabbitmq_url, log_level=logging.DEBUG)
app = FastStream(broker)

exchange = RabbitExchange(
    "main",
    type=ExchangeType.TOPIC,
    auto_delete=False,
    durable=True,
)
publish_queue = RabbitQueue(
    name="publish",
    durable=True,
    auto_delete=True,
    routing_key="mails.parsed",
)

subscribe_queue = RabbitQueue(
    name="publish",
    durable=True,
    auto_delete=True,
    routing_key="events.mails",
)


@broker.subscriber(subscribe_queue)
async def handle(message: str):
    result: EventInfo = pipeline(message)
    if result is None:
        return

    await broker.publish(asdict(result), publish_queue)
