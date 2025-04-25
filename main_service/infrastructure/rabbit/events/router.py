from dishka import FromDishka
from faststream.rabbit import (
    ExchangeType,
    RabbitExchange,
    RabbitQueue,
    RabbitRouter,
)

from application.events.dtos import EventInfo
from application.events.usecases import DeduplicateEventUseCase
from infrastructure.rabbit.events.mappers import (
    map_event_info_from_pydantic,
    map_event_info_to_create_dto,
)
from infrastructure.rabbit.events.models import EventInfoModel

router = RabbitRouter()

exchange = RabbitExchange(
    "main",
    type=ExchangeType.TOPIC,
    auto_delete=False,
    durable=True,
)

queue = RabbitQueue(
    name="process-events",
    durable=True,
    auto_delete=True,
    routing_key="mails.parsed",
)


@router.subscriber(queue, exchange)
async def consume(
    model: EventInfoModel, deduplicate: FromDishka[DeduplicateEventUseCase]
):
    event_info: EventInfo = map_event_info_from_pydantic(model)
    dto = map_event_info_to_create_dto(event_info)
    return await deduplicate(event_info.mail_id, dto)
