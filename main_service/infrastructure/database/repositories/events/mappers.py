from adaptix import P
from adaptix.conversion import (
    allow_unlinked_optional,
    link_function,
)
from domain.events.dtos import CreateEventDto
from domain.events.entities import Event

from infrastructure.database.mappers import postgres_retort

from .models import EventDatabaseModel

retort = postgres_retort.extend(recipe=[])

map_from_db = retort.get_converter(
    EventDatabaseModel,
    Event,
)

map_to_db = retort.get_converter(
    Event,
    EventDatabaseModel,
    recipe=[
        link_function(
            lambda event: event.id,
            P[EventDatabaseModel].id,
        ),
        link_function(
            lambda event: event.created_at,
            P[EventDatabaseModel].created_at,
        ),
    ],
)

map_create_dto_to_model = retort.get_converter(
    CreateEventDto,
    EventDatabaseModel,
    recipe=[
        allow_unlinked_optional(P[EventDatabaseModel].id),
        allow_unlinked_optional(P[EventDatabaseModel].is_visible),
        allow_unlinked_optional(P[EventDatabaseModel].created_at),
        link_function(
            lambda dto: dto.organization_id,
            P[EventDatabaseModel].organization_id,
        ),
    ],
)
