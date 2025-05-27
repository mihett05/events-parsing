from datetime import datetime

from adaptix import P
from adaptix.conversion import allow_unlinked_optional, coercer, link_function
from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment
from domain.mails.dtos import CreateMailDto
from domain.mails.entities import Mail

from infrastructure.mocks.mappers import mock_retort
from infrastructure.mocks.repositories.attachments.mappers import (
    map_create_dto_to_entity as attachment_create_dto_mapper,
)

count = 0


def inc():
    global count
    count += 1
    return count


retort = mock_retort.extend(recipe=[])

map_create_dto_to_entity = retort.get_converter(
    CreateMailDto,
    Mail,
    recipe=[
        link_function(
            lambda dto: inc(),
            P[Mail].id,
        ),
        link_function(
            lambda dto: datetime.now(),
            P[Mail].created_at,
        ),
        allow_unlinked_optional(P[Mail].event_id),
        allow_unlinked_optional(P[Mail].retry_after),
        coercer(
            CreateAttachmentDto,
            Attachment,
            attachment_create_dto_mapper,
        ),
    ],
)
