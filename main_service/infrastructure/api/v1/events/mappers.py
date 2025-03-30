from adaptix import P
from adaptix.conversion import link_function

from application.events.dtos import UpdateEventDto
from domain.events.dtos import CreateEventDto
from domain.events.entities import Event
from infrastructure.api.retort import pydantic_retort
from .dtos import (
    CreateEventModelDto,
    UpdateEventModelDto,
)
from .models import EventModel

retort = pydantic_retort.extend(recipe=[])

map_create_dto_from_pydantic = retort.get_converter(
    CreateEventModelDto, CreateEventDto
)


@retort.impl_converter(
    recipe=[
        link_function(
            lambda event: event.id,
            P[EventModel].id,
        )
    ]
)
def map_to_pydantic(event: Event) -> EventModel: ...


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
