from adaptix import P
from adaptix.conversion import link_function
from application.events.dtos import UpdateEventDto
from domain.events.dtos import CreateEventDto, ReadAllEventsFeedDto, ReadAllEventsDto
from domain.events.entities import Event

from infrastructure.api.retort import pydantic_retort

from .dtos import (
    CreateEventModelDto,
    ReadAllEventsFeedModelDto,
    UpdateEventModelDto, ReadAllEventsCalendarModelDto,
)
from .models import EventModel

retort = pydantic_retort.extend(recipe=[])

map_create_dto_from_pydantic = retort.get_converter(
    CreateEventModelDto, CreateEventDto
)
map_read_all_dto_from_pydantic = retort.get_converter(
    ReadAllEventsFeedModelDto, ReadAllEventsFeedDto
)
map_read_all_dto_calendar_from_pydantic = retort.get_converter(
    ReadAllEventsCalendarModelDto, ReadAllEventsDto
)

map_to_pydantic = retort.get_converter(
    Event,
    EventModel,
    recipe=[
        link_function(
            lambda event: event.id,
            P[EventModel].id,
        ),
        link_function(
            lambda event: event.created_at,
            P[EventModel].created_at,
        ),
        link_function(
            lambda event: event.organization_id,
            P[EventModel].organization_id,
        ),
    ],
)


@retort.impl_converter(
    recipe=[
        link_function(
            lambda dto, event_id: event_id,
            P[UpdateEventDto].event_id,
        )
    ]
)
def map_update_dto_from_pydantic(
    dto: UpdateEventModelDto, event_id: int
) -> UpdateEventDto: ...
