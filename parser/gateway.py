from dataclasses import asdict

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from parser.events import EventInfo
from parser.pipeline import pipeline

broker = RabbitBroker()
app = FastStream(broker)


@broker.subscriber("test")
async def handle(message: str):
    print(message)
    return
    result: EventInfo = pipeline(message)
    if result is None:
        return

    await broker.publish(asdict(result))


@app.after_startup
async def test_publish():
    await broker.publish(
        "message",
        "test",
    )
