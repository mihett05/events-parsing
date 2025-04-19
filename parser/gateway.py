import asyncio
import logging
from dataclasses import asdict
from typing import Iterable

from faststream import FastStream
from faststream.rabbit import (
    ExchangeType,
    RabbitBroker,
    RabbitExchange,
    RabbitQueue,
)

from config import get_config
from events import DatesInfo, EventInfo
from hackathonrf_parser import parser as parse_data
from pipeline import pipeline

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
    name="process-events",
    durable=True,
    auto_delete=True,
    routing_key="mails.parsed",
)

subscribe_queue = RabbitQueue(
    name="process-mails",
    durable=True,
    auto_delete=True,
    routing_key="events.mails",
)


async def start_parsing():
    data: Iterable[EventInfo] = parse_data()
    for event in data:
        await broker.publish(asdict(event), publish_queue, exchange=exchange)


@app.after_startup
async def fill_data():
    asyncio.create_task(start_parsing())


@broker.subscriber(subscribe_queue)
async def handle(message: str):
    result: EventInfo = pipeline(message)
    if result is None:
        return

    await broker.publish(asdict(result), publish_queue)
