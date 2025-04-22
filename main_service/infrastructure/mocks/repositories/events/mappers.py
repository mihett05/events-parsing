from adaptix import P
from adaptix.conversion import (
    allow_unlinked_optional,
)
from domain.events.dtos import CreateEventDto
from domain.events.entities import Event
<<<<<<< HEAD

from infrastructure.database.mappers import postgres_retort
=======
>>>>>>> 734238dad51cb720fbb31b35c5efe9ed046573b5

from infrastructure.mocks.mappers import mock_retort

retort = mock_retort.extend(recipe=[])


@retort.impl_converter(
    recipe=[
        allow_unlinked_optional(P[Event].id),
        allow_unlinked_optional(P[Event].is_visible),
        allow_unlinked_optional(P[Event].created_at),
    ]
)
def map_create_dto_to_entity(dto: CreateEventDto) -> Event: ...
