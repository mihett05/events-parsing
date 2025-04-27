from datetime import datetime

from adaptix import P
from adaptix.conversion import allow_unlinked_optional, coercer, link_function

from application.events.dtos import DatesInfo, EventInfo
from domain.events.dtos import CreateEventDto
from infrastructure.api.retort import pydantic_retort
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
