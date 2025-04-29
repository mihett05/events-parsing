# -------------------------------------------------------
# ------------------- ATTACHMENTS -----------------------
# -------------------------------------------------------
import pytest

from httpx import AsyncClient

from infrastructure.api.v1.attachments.models import AttachmentModel


@pytest.mark.asyncio
async def test_create_attachments(async_client: AsyncClient, user_with_token_model_factory):
    headers = {"Authorization": f"Bearer {user_with_token_model_factory.access_token}"}

    file_content = b"Fake file content"
    files = {
        'files': ('test.jpg', file_content, 'image/jpeg')
    }

    response = await async_client.post("/v1/attachments/1", files=files, headers=headers)
    assert response.status_code == 200
    result = [AttachmentModel(**a) for a in response.json()]
    assert len(result) > 0
    assert result[0].extension == ".jpg"


@pytest.mark.asyncio
async def test_read_attachment(async_client: AsyncClient, user_with_token_model_factory, attachment_model_factory):
    user = await user_with_token_model_factory()
    attachment = attachment_model_factory()
    headers = {"Authorization": f"Bearer {user.access_token}"}
    response = await async_client.get(f"/v1/attachments/{attachment.id}", headers=headers)
    if response.status_code == 200:
        result = AttachmentModel(**response.json())
        assert result.id == attachment.id
    else:
        assert response.status_code == 404