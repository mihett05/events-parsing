import pytest
from application.attachments.usecases import ReadAttachmentUseCase


@pytest.mark.asyncio
async def test_read_success(
    create_attachment,
    read_attachment_usecase: ReadAttachmentUseCase,
    get_admin,
):
    # TODO: Тоже трабл с бд
    attachment = await read_attachment_usecase(create_attachment.id, get_admin)
    attrs = ("id", "filename", "extension", "mail_id", "event_id", "created_at")
    for attr in attrs:
        assert getattr(attachment, attr) == getattr(create_attachment, attr)
