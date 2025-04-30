from adaptix import P
from adaptix.conversion import allow_unlinked_optional, link_function
from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment

from infrastructure.mocks.mappers import mock_retort

retort = mock_retort.extend(recipe=[])

map_create_dto_to_entity = retort.get_converter(
    CreateAttachmentDto,
    Attachment,
    recipe=[
        allow_unlinked_optional(P[Attachment].file_link),
        allow_unlinked_optional(P[Attachment].created_at),
        link_function(
            lambda attachment: attachment.mail and attachment.mail.id,
            P[Attachment].mail_id,
        ),
        link_function(
            lambda attachment: attachment.event and attachment.event.id,
            P[Attachment].event_id,
        ),
    ],
)
