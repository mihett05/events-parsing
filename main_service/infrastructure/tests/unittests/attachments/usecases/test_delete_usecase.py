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
    create_attachment,
    attachments_repository: AttachmentsRepository,
    read_attachment_usecase: ReadAttachmentUseCase,
):
    create_attachment = await create_attachment()
    deleted_attachment = await delete_attachment_usecase(
        create_attachment.id, None
    )
    attrs = ("id", "filename", "extension", "mail_id", "event_id", "created_at")
    for attr in attrs:
        assert getattr(deleted_attachment, attr) == getattr(
            create_attachment, attr
        )

    with pytest.raises(AttachmentNotFoundError):
        await read_attachment_usecase(deleted_attachment.id, None)
