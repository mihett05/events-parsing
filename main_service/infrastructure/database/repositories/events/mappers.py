from adaptix import P
from adaptix.conversion import (
    allow_unlinked_optional,
    coercer,
    link_function,
)
from domain.attachments.entities import Attachment
from domain.events.dtos import CreateEventDto
from domain.events.entities import Event

from infrastructure.database.mappers import postgres_retort
from infrastructure.database.repositories.attachments.mappers import (
    map_from_db as attachment_map_from_db,
)
from infrastructure.database.repositories.attachments.mappers import (
    map_to_db as attachment_map_to_db,
)

from ..attachments import AttachmentDatabaseModel
from .models import EventDatabaseModel

retort = postgres_retort.extend(recipe=[])

map_from_db = retort.get_converter(
    EventDatabaseModel,
    Event,
    recipe=[
        allow_unlinked_optional(P[Event].members),
        coercer(AttachmentDatabaseModel, Attachment, attachment_map_from_db),
    ],
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
        coercer(Attachment, AttachmentDatabaseModel, attachment_map_to_db),
    ],
)

map_create_dto_to_model = retort.get_converter(
    CreateEventDto,
    EventDatabaseModel,
    recipe=[
        allow_unlinked_optional(P[EventDatabaseModel].id),
        allow_unlinked_optional(P[EventDatabaseModel].is_visible),
        allow_unlinked_optional(P[EventDatabaseModel].created_at),
        allow_unlinked_optional(P[EventDatabaseModel].attachments),
        link_function(
            lambda dto: dto.organization_id,
            P[EventDatabaseModel].organization_id,
        ),
    ],
)
