import pytest
from application.attachments.gateways import FilesGateway
from application.attachments.usecases import (
    ReadAttachmentUseCase,
)
from domain.attachments.exceptions import AttachmentNotFoundError
from domain.attachments.repositories import AttachmentsRepository


@pytest.mark.asyncio
async def test_delete_success(
    files_gateway: FilesGateway,
    create_attachment,
    attachments_repository: AttachmentsRepository,
    read_attachment_usecase: ReadAttachmentUseCase,
    get_admin,
):
    deleted_attachment = await files_gateway.delete(create_attachment)
    assert deleted_attachment == create_attachment
    with pytest.raises(AttachmentNotFoundError):
        await read_attachment_usecase(deleted_attachment.id, get_admin)
