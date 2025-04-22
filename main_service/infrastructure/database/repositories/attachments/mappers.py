from adaptix import P
from adaptix.conversion import allow_unlinked_optional

from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment
from infrastructure.database.mappers import postgres_retort

from .models import AttachmentDatabaseModel

retort = postgres_retort.extend(recipe=[])

map_from_db = retort.get_converter(
    AttachmentDatabaseModel,
    Attachment,
    recipe=[
        allow_unlinked_optional(P[Attachment].content),
    ],
)

map_to_db = retort.get_converter(
    Attachment,
    AttachmentDatabaseModel,
    recipe=[
        allow_unlinked_optional(P[AttachmentDatabaseModel].owner_id),
        allow_unlinked_optional(P[AttachmentDatabaseModel].event_id),
        allow_unlinked_optional(P[AttachmentDatabaseModel].created_at),
    ],
)

map_create_dto_to_model = retort.get_converter(
    CreateAttachmentDto,
    AttachmentDatabaseModel,
    recipe=[
        allow_unlinked_optional(P[AttachmentDatabaseModel].owner_id),
        allow_unlinked_optional(P[AttachmentDatabaseModel].event_id),
        allow_unlinked_optional(P[AttachmentDatabaseModel].created_at),
    ],
)
