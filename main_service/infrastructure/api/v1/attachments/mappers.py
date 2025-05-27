from pathlib import Path
from uuid import UUID

from adaptix import P
from adaptix.conversion import link_function
from domain.attachments.dtos import CreateAttachmentDto, UpdateAttachmentDto
from domain.attachments.entities import Attachment
from domain.events.entities import Event
from fastapi import UploadFile

from infrastructure.api.retort import pydantic_retort

from .dtos import UpdateAttachmentModelDto
from .models import AttachmentModel

retort = pydantic_retort.extend(recipe=[])


@retort.impl_converter(
    recipe=[
        link_function(
            lambda dto, attachment_id: attachment_id,
            P[UpdateAttachmentDto].attachment_id,
        )
    ]
)
def map_update_dto_from_pydantic(
    dto: UpdateAttachmentModelDto,
    attachment_id: UUID,  # noqa
) -> UpdateAttachmentDto: ...


"""Конвертирует Pydantic DTO в доменный DTO для обновления вложения."""

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
"""Конвертер для трансформации доменной модели Attachment в Pydantic модель.
Преобразует поля created_at и file_link в подходящий формат."""


def map_file_to_dto(file: UploadFile, event: Event) -> CreateAttachmentDto:
    """Преобразует загруженный файл в DTO для создания вложения.

    Извлекает имя и расширение файла, сохраняет содержимое
    и связывает с соответствующим событием.
    """
    return CreateAttachmentDto(
        filename=Path(file.filename).stem,
        extension=Path(file.filename).suffix.lower(),
        content=file.file,
        event=event,
    )
