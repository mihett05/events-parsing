import pytest

from application.attachments.usecases import CreateAttachmentUseCase
from domain.attachments.dtos import CreateAttachmentDto


@pytest.mark.asyncio
async def test_create_success(
    create_attachment_usecase: CreateAttachmentUseCase,
    create_attachment_dtos: list[CreateAttachmentDto],
):
    succeed, failed = await create_attachment_usecase(create_attachment_dtos, None)
    assert len(failed) == 0
    assert len(succeed) == len(create_attachment_dtos)

    succeed, failed = await create_attachment_usecase(
        [create_attachment_dtos[0]], None
    )
    assert succeed == 0
    assert (
        failed[0]
        == create_attachment_dtos[0].filename
        + create_attachment_dtos[0].extension
    )
