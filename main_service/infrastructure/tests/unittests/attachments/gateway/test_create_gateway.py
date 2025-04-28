from typing import BinaryIO

import pytest
from application.attachments.gateways import FilesGateway
from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.repositories import AttachmentsRepository


@pytest.mark.asyncio
async def test_create_success(
    files_gateway: FilesGateway,
    create_attachment_dtos: list[CreateAttachmentDto],
    attachments_repository: AttachmentsRepository,
    create_attachment_content: BinaryIO,
):
    attachment = await attachments_repository.create(create_attachment_dtos[0])
    assert attachment == await files_gateway.create(
        attachment, create_attachment_content
    )
