import pytest

from application.attachments.usecases import (
    DeleteAttachmentUseCase,
    ReadAttachmentUseCase,
)
from domain.attachments.entities import Attachment
from domain.attachments.exceptions import AttachmentNotFoundError
from domain.attachments.repositories import AttachmentsRepository


@pytest.mark.asyncio
async def test_delete_success(
    delete_attachment_usecase: DeleteAttachmentUseCase,
    create_attachment: Attachment,
    attachments_repository: AttachmentsRepository,
    read_attachment_usecase: ReadAttachmentUseCase,
):
    deleted_attachment = await delete_attachment_usecase(
        create_attachment.id, None
    )
    assert deleted_attachment == create_attachment

    with pytest.raises(AttachmentNotFoundError):
        await read_attachment_usecase(deleted_attachment.id, None)
