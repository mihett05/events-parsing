from adaptix import P
from adaptix.conversion import (
    allow_unlinked_optional,
)
from domain.mails.dtos import CreateMailDto
from domain.mails.entities import Mail

from infrastructure.database.mappers import postgres_retort

retort = postgres_retort.extend(recipe=[])


@retort.impl_converter(
    recipe=[
        allow_unlinked_optional(P[Mail].user_id),
        allow_unlinked_optional(P[Mail].event_id),
        allow_unlinked_optional(P[Mail].created_at),
        allow_unlinked_optional(P[Mail].retry_after),
    ]
)
def map_create_dto_to_entity(dto: CreateMailDto) -> Mail: ...
