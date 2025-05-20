from adaptix import P
from adaptix.conversion import allow_unlinked_optional, coercer, link_function
from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment
from domain.mails.dtos import CreateMailDto
from domain.mails.entities import Mail

from infrastructure.database.mappers import postgres_retort
from infrastructure.database.repositories.attachments.mappers import (
    map_create_dto_to_model as attachment_create_dto_mapper,
)
from infrastructure.database.repositories.attachments.mappers import (
    map_from_db as attachment_from_db_mapper,
)
from infrastructure.database.repositories.attachments.mappers import (
    map_to_db as attachment_to_db_mapper,
)

from ..attachments import AttachmentDatabaseModel
from .models import MailDatabaseModel

retort = postgres_retort.extend(recipe=[])

map_from_db = retort.get_converter(
    MailDatabaseModel,
    Mail,
    recipe=[coercer(AttachmentDatabaseModel, Attachment, attachment_from_db_mapper)],
)

map_to_db = retort.get_converter(
    Mail,
    MailDatabaseModel,
    recipe=[
        link_function(
            lambda mail: mail.id,
            P[MailDatabaseModel].id,
        ),
        link_function(
            lambda mail: mail.event_id,
            P[MailDatabaseModel].event_id,
        ),
        coercer(Attachment, AttachmentDatabaseModel, attachment_to_db_mapper),
    ],
)

map_create_dto_to_model = retort.get_converter(
    CreateMailDto,
    MailDatabaseModel,
    recipe=[
        allow_unlinked_optional(P[MailDatabaseModel].id),
        allow_unlinked_optional(P[MailDatabaseModel].event_id),
        allow_unlinked_optional(P[MailDatabaseModel].created_at),
        allow_unlinked_optional(P[MailDatabaseModel].retry_after),
        coercer(
            CreateAttachmentDto,
            AttachmentDatabaseModel,
            attachment_create_dto_mapper,
        ),
    ],
)
