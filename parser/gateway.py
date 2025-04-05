import logging
from dataclasses import asdict

from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue

from parser.config import get_config
from parser.events import EventInfo
from parser.pipeline import pipeline

config = get_config()
broker = RabbitBroker(config.rabbitmq_url, log_level=logging.DEBUG)
app = FastStream(broker)
publish_queue = RabbitQueue(config.rabbitmq_queue)
subscribe_queue = RabbitQueue(
    config.rabbitmq_queue,
    auto_delete=True,
)


@broker.subscriber(subscribe_queue)
async def handle(message: str):
    result: EventInfo = pipeline(message)
    if result is None:
        return

    await broker.publish(asdict(result), publish_queue)
