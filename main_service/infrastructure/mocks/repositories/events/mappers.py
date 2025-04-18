from adaptix import P
from adaptix._internal.conversion.facade.provider import (
    allow_unlinked_optional,
)
from domain.events.dtos import CreateEventDto
from domain.events.entities import Event

from infrastructure.database.mappers import postgres_retort

retort = postgres_retort.extend(recipe=[])


@retort.impl_converter(
    recipe=[
        allow_unlinked_optional(P[Event].id),
        allow_unlinked_optional(P[Event].is_visible),
        allow_unlinked_optional(P[Event].created_at),
    ]
)
def map_create_dto_to_entity(dto: CreateEventDto) -> Event: ...
