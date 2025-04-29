from adaptix import P
from adaptix.conversion import allow_unlinked_optional, coercer
from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment
from domain.mails.dtos import CreateMailDto
from domain.mails.entities import Mail

from infrastructure.mocks.mappers import mock_retort
from infrastructure.mocks.repositories.attachments.mappers import (
    map_create_dto_to_entity as attachment_create_dto_mapper,
)

retort = mock_retort.extend(recipe=[])

map_create_dto_to_entity = retort.get_converter(
    CreateMailDto,
    Mail,
    recipe=[
        allow_unlinked_optional(P[Mail].id),
        allow_unlinked_optional(P[Mail].event_id),
        allow_unlinked_optional(P[Mail].created_at),
        allow_unlinked_optional(P[Mail].retry_after),
        coercer(
            CreateAttachmentDto,
            Attachment,
            attachment_create_dto_mapper,
        ),
    ],
)
