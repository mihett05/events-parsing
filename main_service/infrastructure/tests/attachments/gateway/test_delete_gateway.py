import pytest
from application.attachments.gateways import FilesGateway
from application.attachments.usecases import (
    CreateAttachmentUseCase,
    DeleteAttachmentUseCase,
    ReadAttachmentUseCase,
)
from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment
from domain.attachments.exceptions import AttachmentNotFoundError
from domain.attachments.repositories import AttachmentsRepository

from infrastructure.tests.attachments.conftest import attachments_repository
from infrastructure.tests.attachments.usecases.conftest import (
    read_attachment_usecase,
)
from infrastructure.tests.users.usecases.conftest import read_user_usecase


@pytest.mark.asyncio
async def test_delete_success(
    files_gateway: FilesGateway,
    create_attachment: Attachment,
    attachments_repository: AttachmentsRepository,
    read_attachment_usecase: ReadAttachmentUseCase,
):
    deleted_attachment = await files_gateway.delete(create_attachment)
    assert deleted_attachment == create_attachment
    with pytest.raises(AttachmentNotFoundError):
        await read_attachment_usecase(deleted_attachment.id, None)
