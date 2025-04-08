from datetime import datetime

from adaptix.conversion import coercer
from application.events.dtos import DatesInfo, EventInfo

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
