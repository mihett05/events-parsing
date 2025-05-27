from datetime import datetime

from adaptix import P
from adaptix.conversion import allow_unlinked_optional, coercer, link_function
from application.events.dtos import DatesInfo, EventInfo
from domain.events.dtos import CreateEventDto
from domain.mails.entities import Mail

from infrastructure.api.retort import pydantic_retort
from infrastructure.rabbit.events.models import (
    DatesInfoModel,
    EventInfoModel,
    MailModel,
)

retort = pydantic_retort.extend(recipe=[])

map_event_info_dates_from_pydantic = retort.get_converter(
    DatesInfoModel,
    DatesInfo,
    recipe=[coercer(str, datetime, lambda dt: datetime.strptime(dt, "%d-%m-%Y"))],
)
"""Конвертирует модель данных о датах в DTO, преобразуя строки в datetime."""


map_event_info_from_pydantic = retort.get_converter(
    EventInfoModel,
    EventInfo,
    recipe=[
        coercer(DatesInfoModel, DatesInfo, map_event_info_dates_from_pydantic),
    ],
)
"""Конвертирует модель информации о событии в соответствующий DTO."""


map_event_info_to_create_dto = retort.get_converter(
    EventInfo,
    CreateEventDto,
    recipe=[
        link_function(
            lambda event_info: event_info.dates.end_date,
            P[CreateEventDto].end_date,
        ),
        link_function(
            lambda event_info: event_info.dates.start_date,
            P[CreateEventDto].start_date,
        ),
        link_function(
            lambda event_info: event_info.dates.end_registration,
            P[CreateEventDto].end_registration,
        ),
        allow_unlinked_optional(P[CreateEventDto].organization_id),
    ],
)
"""Преобразует информацию о событии в DTO для создания события."""


map_mail_to_pydantic = retort.get_converter(
    Mail,
    MailModel,
    recipe=[
        link_function(
            lambda entity: [
                attachment.file_link
                for attachment in entity.attachments
                if attachment.file_link
            ],
            P[MailModel].attachments,
        )
    ],
)
"""Конвертирует сущность письма в Pydantic модель для RabbitMQ."""
