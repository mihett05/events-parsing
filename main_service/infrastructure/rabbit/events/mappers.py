from datetime import datetime

from adaptix import P
from adaptix._internal.conversion.facade.provider import link_function
from adaptix.conversion import coercer

from application.events.dtos import DatesInfo, EventInfo
from domain.events.dtos import CreateEventDto
from infrastructure.api.retort import pydantic_retort
from infrastructure.api.v1.events.models import EventModel
from infrastructure.rabbit.events.models import (
    DatesInfoModel,
    EventInfoModel,
)

retort = pydantic_retort.extend(recipe=[])

map_event_info_dates_from_pydantic = retort.get_converter(
    DatesInfoModel,
    DatesInfo,
    recipe=[
        coercer(str, datetime, lambda dt: datetime.strptime(dt, "%d-%m-%Y"))
    ],
)
map_event_info_from_pydantic = retort.get_converter(
    EventInfoModel,
    EventInfo,
    recipe=[
        coercer(DatesInfoModel, DatesInfo, map_event_info_dates_from_pydantic),
    ],
)


@retort.impl_converter(
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
    ]
)
def map_event_info_to_create_dto(event_info: EventInfo) -> CreateEventDto: ...
