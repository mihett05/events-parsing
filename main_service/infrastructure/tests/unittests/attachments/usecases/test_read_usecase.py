import pytest
from application.attachments.usecases import ReadAttachmentUseCase
from domain.attachments.entities import Attachment


@pytest.mark.asyncio
async def test_read_success(
    create_attachment,
    read_attachment_usecase: ReadAttachmentUseCase,
):
    create_attachment = await create_attachment()
    attachment = await read_attachment_usecase(create_attachment.id, None)
    attrs = ("id", "filename", "extension", "mail_id", "event_id", "created_at")
    for attr in attrs:
        assert getattr(attachment, attr) == getattr(create_attachment, attr)
