from parser.events import Event
from pathlib import Path

from adaptix import P
from adaptix.conversion import link_function
from fastapi import UploadFile

from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment
from infrastructure.api.retort import pydantic_retort

from .models import AttachmentModel

retort = pydantic_retort.extend(recipe=[])


map_to_pydantic = retort.get_converter(
    Attachment,
    AttachmentModel,
    recipe=[
        link_function(
            lambda attachment: attachment.created_at,
            P[AttachmentModel].created_at,
        ),
        link_function(
            lambda attachment: str(attachment.file_link),
            P[AttachmentModel].file_link,
        ),
    ],
)


def map_file_to_dto(file: UploadFile, event: Event) -> CreateAttachmentDto:
    return CreateAttachmentDto(
        filename=Path(file.filename).stem,
        extension=Path(file.filename).suffix.lower(),
        content=file.file,
        event=event,
    )
