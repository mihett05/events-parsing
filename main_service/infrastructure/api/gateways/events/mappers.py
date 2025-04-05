from datetime import datetime

from adaptix.conversion import coercer

from application.events.dtos import EventInfo, DatesInfo
from infrastructure.api.gateways.events.models import (
    EventInfoModel,
    DatesInfoModel,
)
from infrastructure.api.retort import pydantic_retort

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
