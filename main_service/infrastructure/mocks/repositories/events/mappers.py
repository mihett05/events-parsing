from adaptix import P
from adaptix.conversion import (
    allow_unlinked_optional,
)
from domain.events.dtos import CreateEventDto
from domain.events.entities import Event

from infrastructure.mocks.mappers import mock_retort

retort = mock_retort.extend(recipe=[])


# TODO: Переписать маппер
@retort.impl_converter(
    recipe=[
        allow_unlinked_optional(P[Event].id),
        allow_unlinked_optional(P[Event].is_visible),
        allow_unlinked_optional(P[Event].created_at),
        allow_unlinked_optional(P[Event].members),
    ]
)
def map_create_dto_to_entity(dto: CreateEventDto) -> Event: ...  # noqa
