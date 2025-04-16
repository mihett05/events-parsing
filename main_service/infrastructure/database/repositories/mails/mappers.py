from adaptix import P
from adaptix._internal.conversion.facade.provider import (
    allow_unlinked_optional,
    link_function,
)

from domain.mails.dtos import CreateMailDto
from domain.mails.entities import Mail
from infrastructure.database.mappers import postgres_retort

from .models import MailDatabaseModel

retort = postgres_retort.extend(recipe=[])

map_from_db = retort.get_converter(
    MailDatabaseModel,
    Mail,
)


@retort.impl_converter(
    recipe=[
        link_function(
            lambda mail: mail.id,
            P[MailDatabaseModel].id,
        ),
        link_function(
            lambda mail: mail.event_id,
            P[MailDatabaseModel].event_id,
        ),
    ]
)
def map_to_db(mail: Mail) -> MailDatabaseModel: ...


@retort.impl_converter(
    recipe=[
        allow_unlinked_optional(P[MailDatabaseModel].id),
        allow_unlinked_optional(P[MailDatabaseModel].event_id),
        allow_unlinked_optional(P[MailDatabaseModel].created_at),
        allow_unlinked_optional(P[MailDatabaseModel].ded_line),
    ]
)
def map_create_dto_to_model(dto: CreateMailDto) -> MailDatabaseModel: ...
