from adaptix import P
from adaptix.conversion import allow_unlinked_optional
from domain.mails.dtos import CreateMailDto, ParsedMailInfoDto

from infrastructure.api.retort import pydantic_retort

retort = pydantic_retort.extend(recipe=[])

map_mail_info_to_create_dto = retort.get_converter(
    ParsedMailInfoDto,
    CreateMailDto,
    recipe=[
        allow_unlinked_optional(P[CreateMailDto].state),
        allow_unlinked_optional(P[CreateMailDto].retry_after),
    ],
)
