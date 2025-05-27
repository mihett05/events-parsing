from application.events.dtos import EventInfo
from application.events.usecases import DeduplicateEventUseCase
from dishka import FromDishka
from faststream.rabbit import (
    ExchangeType,
    RabbitExchange,
    RabbitQueue,
    RabbitRouter,
)

from infrastructure.rabbit.events.mappers import (
    map_event_info_from_pydantic,
    map_event_info_to_create_dto,
)
from infrastructure.rabbit.events.models import EventInfoModel

router = RabbitRouter()
"""Роутер для обработки событий через RabbitMQ."""


exchange = RabbitExchange(
    "main",
    type=ExchangeType.TOPIC,
    auto_delete=False,
    durable=True,
)
"""Обменник для маршрутизации сообщений о событиях."""


queue = RabbitQueue(
    name="process-events",
    durable=True,
    auto_delete=True,
    routing_key="mails.parsed",
)
"""Очередь для обработки событий, полученных из писем."""


@router.subscriber(queue, exchange)
async def consume(
    model: EventInfoModel, deduplicate: FromDishka[DeduplicateEventUseCase]
):
    """
    Обрабатывает входящие сообщения о событиях.

    Преобразует модель в DTO, выполняет дедупликацию и обработку события.
    """
    event_info: EventInfo = map_event_info_from_pydantic(model)
    dto = map_event_info_to_create_dto(event_info)
    return await deduplicate(event_info.mail_id, dto)
