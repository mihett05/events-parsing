from adaptix import P
from adaptix.conversion import allow_unlinked_optional, coercer
from domain.attachments.dtos import CreateAttachmentDto, ParsedAttachmentInfoDto
from domain.mails.dtos import CreateMailDto, ParsedMailInfoDto

from infrastructure.api.retort import pydantic_retort

retort = pydantic_retort.extend(recipe=[])

map_attachment_to_create_dto = retort.get_converter(
    ParsedAttachmentInfoDto,
    CreateAttachmentDto,
    recipe=[
        allow_unlinked_optional(P[CreateAttachmentDto].mail),
        allow_unlinked_optional(P[CreateAttachmentDto].event),
        allow_unlinked_optional(P[CreateAttachmentDto].id),
    ],
)

map_mail_info_to_create_dto = retort.get_converter(
    ParsedMailInfoDto,
    CreateMailDto,
    recipe=[
        coercer(
            ParsedAttachmentInfoDto,
            CreateAttachmentDto,
            map_attachment_to_create_dto,
        ),
        allow_unlinked_optional(P[CreateMailDto].state),
        allow_unlinked_optional(P[CreateMailDto].retry_after),
    ],
)
