import pytest
from application.attachments.usecases import CreateAttachmentUseCase
from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.exceptions import AttachmentAlreadyExistsError


@pytest.mark.asyncio
async def test_create_success(
    create_attachment_usecase: CreateAttachmentUseCase,
    create_attachment_dtos: list[CreateAttachmentDto],
):
    succeed, failed = await create_attachment_usecase(create_attachment_dtos, None)
    assert len(failed) == 0
    assert len(succeed) == len(create_attachment_dtos)

    with pytest.raises(AttachmentAlreadyExistsError):
        await create_attachment_usecase([create_attachment_dtos[0]], None)
