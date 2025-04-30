from adaptix import P
from adaptix.conversion import allow_unlinked_optional, link_function
from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment

from infrastructure.database.mappers import postgres_retort

from .models import AttachmentDatabaseModel

retort = postgres_retort.extend(recipe=[])

map_from_db = retort.get_converter(
    AttachmentDatabaseModel,
    Attachment,
    recipe=[
        allow_unlinked_optional(P[Attachment].file_link),
        link_function(
            lambda attachment: attachment.created_at,
            P[Attachment].created_at,
        ),
    ],
)

map_to_db = retort.get_converter(
    Attachment,
    AttachmentDatabaseModel,
    recipe=[
        link_function(
            lambda attachment: attachment.created_at,
            P[AttachmentDatabaseModel].created_at,
        ),
    ],
)

map_create_dto_to_model = retort.get_converter(
    CreateAttachmentDto,
    AttachmentDatabaseModel,
    recipe=[
        link_function(
            lambda attachment: attachment.mail and attachment.mail.id,
            P[AttachmentDatabaseModel].mail_id,
        ),
        link_function(
            lambda attachment: attachment.event and attachment.event.id,
            P[AttachmentDatabaseModel].event_id,
        ),
        allow_unlinked_optional(P[AttachmentDatabaseModel].created_at),
    ],
)
