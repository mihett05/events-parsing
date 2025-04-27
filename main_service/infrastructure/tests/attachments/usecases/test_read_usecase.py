import pytest

from application.attachments.usecases import ReadAttachmentUseCase
from domain.attachments.entities import Attachment


@pytest.mark.asyncio
async def test_read_success(
    create_attachment: Attachment,
    read_attachment_usecase: ReadAttachmentUseCase,
):
    attachment = await read_attachment_usecase(create_attachment.id, None)
    assert attachment == create_attachment
