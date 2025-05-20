import pytest
from application.attachments.usecases import ReadAttachmentUseCase
from domain.attachments.entities import Attachment


@pytest.mark.asyncio
async def test_read_success(
    create_attachment,
    read_attachment_usecase: ReadAttachmentUseCase,
    create_user1,
):
    create_attachment = await create_attachment()
    user = await create_user1()

    attachment = await read_attachment_usecase(create_attachment.id, user)
    attrs = ("id", "filename", "extension", "mail_id", "event_id", "created_at")
    for attr in attrs:
        assert getattr(attachment, attr) == getattr(create_attachment, attr)
