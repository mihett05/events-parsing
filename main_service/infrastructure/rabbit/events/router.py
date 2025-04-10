from application.events.dtos import EventInfo
from application.events.usecases import DeduplicateEventUseCase
from dishka import FromDishka
from faststream.rabbit import (
    ExchangeType,
    RabbitExchange,
    RabbitQueue,
    RabbitRouter,
)

from infrastructure.rabbit.events.mappers import map_event_info_from_pydantic
from infrastructure.rabbit.events.models import EventInfoModel

router = RabbitRouter()

exchange = RabbitExchange(
    "main",
    type=ExchangeType.TOPIC,
    auto_delete=False,
    durable=True,
)

queue = RabbitQueue(
    name="consume",
    durable=True,
    auto_delete=True,
    routing_key="mails.parsed",
)


@router.subscriber(queue, exchange)
async def consume(
    model: EventInfoModel, deduplicate: FromDishka[DeduplicateEventUseCase]
):
    dto: EventInfo = map_event_info_from_pydantic(model)
    return await deduplicate(dto)
